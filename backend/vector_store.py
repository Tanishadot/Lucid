from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIR = "knowledge/vector"
COLLECTION_NAME = "lucid_patterns"

_embeddings = None
_vectordb = None

def get_vectordb():
    global _embeddings, _vectordb
    
    if _vectordb is None:
        print("Initializing persistent VectorDB...")
        
        # Create persist directory if it doesn't exist
        os.makedirs(PERSIST_DIR, exist_ok=True)
        
        # Initialize embeddings once
        _embeddings = OpenAIEmbeddings()
        
        # Create persistent Chroma client
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        
        # Initialize vector store with persistent client
        _vectordb = Chroma(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding_function=_embeddings
        )
        
        print("VectorDB initialized successfully")
    
    return _vectordb

def get_embeddings():
    """Get embeddings instance (singleton)"""
    global _embeddings
    
    if _embeddings is None:
        print("Initializing embeddings...")
        _embeddings = OpenAIEmbeddings()
        print("Embeddings initialized")
    
    return _embeddings
