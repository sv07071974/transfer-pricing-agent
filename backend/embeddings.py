import os
import logging
from typing import List, Optional

from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings

from utils import get_env_variable

class EmbeddingManager:
    """Class to manage embeddings for the Transfer Pricing agent"""
    
    def __init__(self):
        """Initialize the embedding manager"""
        self.logger = logging.getLogger(__name__)
        self.embedding_model = get_env_variable('EMBEDDING_MODEL', 'text-embedding-ada-002')
        self._embeddings = None
        
    @property
    def embeddings(self) -> Embeddings:
        """Get or initialize embeddings"""
        if self._embeddings is None:
            self.logger.info(f"Initializing embeddings with model: {self.embedding_model}")
            self._embeddings = OpenAIEmbeddings(model=self.embedding_model)
        return self._embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embeddings for a query text"""
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            self.logger.error(f"Error generating query embedding: {str(e)}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents"""
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            self.logger.error(f"Error generating document embeddings: {str(e)}")
            raise