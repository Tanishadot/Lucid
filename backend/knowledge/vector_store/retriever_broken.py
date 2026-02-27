# backend/knowledge/vector_store/retriever.py

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from core.memory.memory_manager import get_memory
import os
import json
import time
import threading

load_dotenv()

PERSIST_DIR = "knowledge/vector_store/db"

# Thread-safe singleton variables
_vectordb = None
_embeddings = None
_lock = threading.Lock()

def get_embeddings():
    """Get embeddings instance (thread-safe lazy initialization)"""
    global _embeddings
    if _embeddings is None:
        with _lock:
            if _embeddings is None:
                print("Initializing OpenAI embeddings...")
                _embeddings = OpenAIEmbeddings()
                print("OpenAI embeddings initialized successfully.")
    return _embeddings

def get_vectordb():
    """Get Chroma vector store (thread-safe lazy initialization)"""
    global _vectordb
    
    if _vectordb is None:
        with _lock:
            if _vectordb is None:
                print("STEP 1: Entered get_vectordb")
                print("OPENAI_API_KEY detected:", bool(os.getenv("OPENAI_API_KEY")))
                
                print("STEP 2: Creating embeddings...")
                embeddings = OpenAIEmbeddings()
                print("STEP 3: Embeddings object created")
                
                print("STEP A: Testing embedding call...")
                try:
                    test_vector = embeddings.embed_query("test")
                    print("STEP B: Embedding successful. Length:", len(test_vector))
                except Exception as e:
                    print("Embedding test failed:", e)
                    raise
                
                print("STEP 4: Before Chroma constructor...")
                _vectordb = Chroma(
                    persist_directory=PERSIST_DIR,
                    embedding_function=embeddings,
                    collection_metadata={"hnsw:space": "cosine"}
                )
                print("STEP 5: After Chroma constructor")
                
                # Check document count
                docs = _vectordb.get()
                doc_count = len(docs['documents'])
                
                print("VECTOR STORE COUNT:", _vectordb._collection.count())
                
                if doc_count == 0:
                    raise Exception("Vector store is empty. Ingestion failed.")
                else:
                    print("Vector store successfully initialized with documents")
                    
                print("=== LAZY CHROMA INITIALIZATION COMPLETE ===")
    
    return _vectordb

class Retriever:
    def __init__(self):
        # Don't initialize in constructor - use lazy loading
        pass
    
    def retrieve(self, user_message: str, k: int = 3):
        try:
            # Lazy load vector store only when needed
            vectordb = get_vectordb()
            embeddings = get_embeddings()
            
            results = vectordb.similarity_search_with_score(user_message, k=k)
            print(f"=== RETRIEVAL DEBUG ===")
            print(f"Query: {user_message}")
            print(f"Retrieved {len(results)} documents with scores:")
            for i, (doc, score) in enumerate(results):
                print(f"  {i+1}. Score: {score:.4f}")
                print(f"     Content: {doc.page_content[:100]}...")
                if doc.metadata:
                    cognitive_pattern = doc.metadata.get('cognitive_pattern', 'N/A')
                    print(f"     Cognitive Pattern: {cognitive_pattern}")
                    reframe = doc.metadata.get('reframe', 'N/A')
                    question = doc.metadata.get('question', 'N/A')
                    print(f"     Reframe: {reframe}")
                    print(f"     Question: {question}")
            print(f"=== END DEBUG ===")
            return results
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []

# Global retriever instance
_retriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever

def compute_pattern_similarity(user_input: str, active_pattern: str) -> float:
    """Compute similarity between user input and active pattern"""
    if not active_pattern:
        return 0.0
    
    try:
        embeddings = get_embeddings()
        
        # Embed both texts
        user_embedding = embeddings.embed_query(user_input)
        pattern_embedding = embeddings.embed_query(active_pattern)
        
        # Compute cosine similarity
        import numpy as np
        user_vec = np.array(user_embedding)
        pattern_vec = np.array(pattern_embedding)
        
        dot_product = np.dot(user_vec, pattern_vec)
        norm_user = np.linalg.norm(user_vec)
        norm_pattern = np.linalg.norm(pattern_vec)
        
        if norm_user == 0 or norm_pattern == 0:
            return 0.0
        
        similarity = dot_product / (norm_user * norm_pattern)
        return float(similarity)
        
    except Exception as e:
        print(f"Pattern similarity computation failed: {e}")
        return 0.0

def retrieve_reflection_unit(user_input: str) -> dict:
    """
    Retrieve optional reflection hint for model reasoning.
    
    Args:
        user_input: The user's input message
        
    Returns:
        dict: {
            "reframe": str (optional hint),
            "cognitive_pattern": str (optional pattern)
        }
    """
    try:
        print("---- MODEL-FIRST RETRIEVAL ----")
        print("User Input:", user_input)
        
        # Get vector store
        vectordb = get_vectordb()
        
        try:
            print("=== RUNNING SIMILARITY SEARCH ===")
            
            expanded_query = f"""
Conversation context:
{get_memory()}

Current input:
{user_input}
""".strip()
            
            results = vectordb.similarity_search_with_score(expanded_query, k=3)
            
            print("SIMILARITY SEARCH COMPLETE")
            print("RESULT COUNT:", len(results))
            
            if results is None:
                raise Exception("Similarity search not executed")
            
            for doc, score in results:
                print("PATTERN:", doc.metadata.get("cognitive_pattern"))
                print("SCORE:", score)
            
            if len(results) == 0:
                print("WARNING: No retrieval results.")
                return {
                    "reframe": "",
                    "cognitive_pattern": ""
                }
            else:
                print("TOP MATCH TEXT:", results[0][0].page_content[:200])
                
                top_result = results[0][0]
                metadata = top_result.metadata or {}
                content = top_result.page_content
                
                # Extract optional hint
                reframe = metadata.get("reframe", "") or metadata.get("core_reframe", "")
                cognitive_pattern = metadata.get("cognitive_pattern", "")
                
                # If not in metadata, try to parse from content
                if not reframe:
                    try:
                        data = json.loads(content)
                        reframe = data.get("reframe", "") or data.get("core_reframe", "")
                    except json.JSONDecodeError:
                        lines = content.split('\n')
                        for line in lines:
                            if line.startswith("reframe:"):
                                reframe = line.replace("reframe:", "").strip()
                                break
                
                print("Retrieved Hint:", reframe[:100] if reframe else "None")
                
                return {
                    "reframe": reframe,
                    "cognitive_pattern": cognitive_pattern
                }
                
        except Exception as e:
            print(f"Vector search failed: {e}")
            return {
                "reframe": "",
                "cognitive_pattern": ""
            }
        
    except Exception as e:
        print(f"Exception in retrieval: {e}")
        return {
            "reframe": "",
            "cognitive_pattern": ""
        }
    finally:
        print("---- MODEL-FIRST RETRIEVAL END ----")