import os
import glob
import logging
import pickle
from typing import List, Tuple, Dict, Optional

# LangChain imports
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Import custom modules
from utils import get_env_variable

class KnowledgeBase:
    """Class to manage the knowledge base for the Transfer Pricing agent"""
    
    def __init__(self):
        """Initialize the knowledge base"""
        self.logger = logging.getLogger(__name__)
        self.documents_path = os.path.join('data', 'documents')
        self.vector_db_path = os.path.join('vector_db', 'faiss_index')
        
        # Settings from environment variables
        self.model_name = get_env_variable('MODEL_NAME', 'gpt-3.5-turbo')
        self.embedding_model = get_env_variable('EMBEDDING_MODEL', 'text-embedding-ada-002')
        self.chunk_size = int(get_env_variable('CHUNK_SIZE', '1000'))
        self.chunk_overlap = int(get_env_variable('CHUNK_OVERLAP', '100'))
        
        # Initialize components to None
        self.vector_store = None
        self.qa_chain = None
        self.embeddings = None

    def initialize(self, force_refresh: bool = False) -> str:
        """Initialize or refresh the knowledge base"""
        # Check if vector database already exists
        if os.path.exists(f"{self.vector_db_path}.pkl") and not force_refresh:
            self.logger.info("Loading existing vector database")
            return self._load_existing_vector_db()
        else:
            self.logger.info("Creating new vector database")
            return self._create_vector_db()

    def _load_existing_vector_db(self) -> str:
        """Load an existing vector database"""
        try:
            # Initialize the embeddings
            self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
            
            # Load the vector store
            self.vector_store = FAISS.load_local(
                self.vector_db_path, 
                self.embeddings
            )
            
            # Create the QA chain
            self._create_qa_chain()
            
            return "Successfully loaded existing knowledge base"
        except Exception as e:
            self.logger.error(f"Error loading vector database: {str(e)}")
            # If loading fails, try creating a new one
            return self._create_vector_db()

    def _create_vector_db(self) -> str:
        """Create a new vector database from documents"""
        try:
            # Get all document paths
            pdf_files = glob.glob(os.path.join(self.documents_path, "**", "*.pdf"), recursive=True)
            
            if not pdf_files:
                raise ValueError(f"No PDF files found in {self.documents_path}")
            
            # Initialize the embeddings
            self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
            
            # Load and process all documents
            documents = []
            for pdf_file in pdf_files:
                self.logger.info(f"Processing document: {pdf_file}")
                loader = PyPDFLoader(pdf_file)
                documents.extend(loader.load())
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=["\n\n", "\n", ".", " ", ""]
            )
            texts = text_splitter.split_documents(documents)
            
            # Create the vector store
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
            
            # Save the vector store
            os.makedirs(os.path.dirname(self.vector_db_path), exist_ok=True)
            self.vector_store.save_local(self.vector_db_path)
            
            # Create the QA chain
            self._create_qa_chain()
            
            return f"Successfully created knowledge base with {len(texts)} text chunks from {len(pdf_files)} documents"
        except Exception as e:
            self.logger.error(f"Error creating vector database: {str(e)}")
            raise

    def _create_qa_chain(self):
        """Create the QA chain with the LLM and retriever"""
        llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        
        # Create a prompt template that includes specific instructions for Transfer Pricing
        template = """You are a Transfer Pricing knowledge agent for UAE tax regulations. 
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Always cite the section or page number from the Transfer Pricing guide if possible.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:"""
        
        # Create the QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            ),
            chain_type_kwargs={
                "prompt": template
            },
            return_source_documents=True
        )

    def ask(self, query: str) -> Tuple[str, List[Dict]]:
        """Ask a question and get an answer with sources"""
        if not self.qa_chain:
            raise ValueError("Knowledge base not initialized. Call initialize() first.")
        
        # Get the answer
        result = self.qa_chain({"query": query})
        
        # Extract the answer
        answer = result.get("result", "")
        
        # Extract source metadata
        sources = []
        source_documents = result.get("source_documents", [])
        for i, doc in enumerate(source_documents):
            sources.append({
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            })
        
        return answer, sources

    def get_documents(self) -> List[str]:
        """Get a list of all documents in the knowledge base"""
        pdf_files = glob.glob(os.path.join(self.documents_path, "**", "*.pdf"), recursive=True)
        return [os.path.relpath(pdf, self.documents_path) for pdf in pdf_files]