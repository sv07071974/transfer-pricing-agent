import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import custom modules
from knowledge_base import KnowledgeBase
from utils import setup_logging

# Load environment variables
load_dotenv()

# Configure logging
logger = setup_logging()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize knowledge base
knowledge_base = KnowledgeBase()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint to check if the API is running"""
    return jsonify({"status": "healthy", "service": "transfer-pricing-agent"})

@app.route('/api/initialize', methods=['POST'])
def initialize_kb():
    """Initialize or refresh the knowledge base from documents"""
    try:
        force_refresh = request.json.get('force_refresh', False)
        result = knowledge_base.initialize(force_refresh=force_refresh)
        return jsonify({"status": "success", "message": result})
    except Exception as e:
        logger.error(f"Error initializing knowledge base: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query():
    """Process a user query and return an answer"""
    try:
        user_query = request.json.get('query', '')
        if not user_query:
            return jsonify({"status": "error", "message": "Query is required"}), 400
        
        # Get the answer from the knowledge base
        answer, sources = knowledge_base.ask(user_query)
        
        return jsonify({
            "status": "success", 
            "answer": answer,
            "sources": sources
        })
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get a list of all documents in the knowledge base"""
    try:
        documents = knowledge_base.get_documents()
        return jsonify({"status": "success", "documents": documents})
    except Exception as e:
        logger.error(f"Error getting documents: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Initialize the knowledge base on startup
    try:
        knowledge_base.initialize()
    except Exception as e:
        logger.error(f"Error during initial knowledge base setup: {str(e)}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('DEBUG', 'False').lower() == 'true')