from typing import List, Dict, Any, Optional, Tuple
import os
import json
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config.settings import settings
from core.utils.logger import logger
from knowledge.embeddings.embedder import Embedder


class VectorStore:
    """Manages vector storage for knowledge retrieval"""
    
    def __init__(self, store_type: Optional[str] = None, store_path: Optional[str] = None):
        self.store_type = store_type or settings.vector_store_type
        self.store_path = store_path or settings.vector_store_path
        self.embedder = Embedder()
        self._store = None
        self._initialized = False
        
        logger.info(f"VectorStore initialized with type: {self.store_type}")
    
    @property
    def store(self):
        """Lazy initialization of vector store"""
        if not self._initialized:
            self._initialize_store()
        return self._store
    
    def _initialize_store(self):
        """Initialize the vector store"""
        try:
            os.makedirs(self.store_path, exist_ok=True)
            
            if self.store_type.lower() == "faiss":
                self._initialize_faiss()
            elif self.store_type.lower() == "chroma":
                self._initialize_chroma()
            else:
                raise ValueError(f"Unsupported vector store type: {self.store_type}")
            
            self._initialized = True
            logger.info(f"Vector store initialized: {self.store_type}")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            # Create empty store for fallback
            self._store = self._create_empty_store()
            self._initialized = True
    
    def _initialize_faiss(self):
        """Initialize FAISS vector store"""
        index_path = os.path.join(self.store_path, "faiss.index")
        
        if os.path.exists(index_path):
            logger.info("Loading existing FAISS index")
            self._store = FAISS.load_local(
                self.store_path,
                self.embedder.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            logger.info("Creating new FAISS index")
            self._store = self._create_empty_store()
    
    def _initialize_chroma(self):
        """Initialize Chroma vector store"""
        chroma_path = os.path.join(self.store_path, "chroma")
        
        self._store = Chroma(
            persist_directory=chroma_path,
            embedding_function=self.embedder.embeddings
        )
    
    def _create_empty_store(self):
        """Create empty vector store"""
        if self.store_type.lower() == "faiss":
            # Create dummy document and index
            dummy_doc = Document(page_content="dummy", metadata={"source": "dummy"})
            dummy_embedding = self.embedder.embed_text("dummy")
            
            # Create FAISS index with dummy data
            self._store = FAISS.from_documents([dummy_doc], self.embedder.embeddings)
            
            # Remove dummy document
            self._store.delete([dummy_doc.metadata.get("id", "dummy")])
            
        elif self.store_type.lower() == "chroma":
            chroma_path = os.path.join(self.store_path, "chroma")
            self._store = Chroma(
                persist_directory=chroma_path,
                embedding_function=self.embedder.embeddings
            )
        
        return self._store
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to vector store"""
        try:
            if self.store_type.lower() == "faiss":
                self._store.add_documents(documents)
                # Save FAISS index
                self._store.save_local(self.store_path)
            else:  # Chroma
                self._store.add_documents(documents)
                self._store.persist()
            
            logger.info(f"Added {len(documents)} documents to {self.store_type}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return False
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar documents"""
        try:
            return self.store.similarity_search(query, k=k)
        except Exception as e:
            logger.error(f"Failed to perform similarity search: {e}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """Search with similarity scores"""
        try:
            return self.store.similarity_search_with_score(query, k=k)
        except Exception as e:
            logger.error(f"Failed to perform similarity search with score: {e}")
            return []
    
    def get_relevant_context(self, query: str, max_context_length: int = 1000) -> str:
        """Get relevant context for query"""
        try:
            docs = self.similarity_search(query, k=3)
            
            context_parts = []
            current_length = 0
            
            for doc in docs:
                content = doc.page_content
                if current_length + len(content) <= max_context_length:
                    context_parts.append(content)
                    current_length += len(content)
                else:
                    # Add partial content if space allows
                    remaining_space = max_context_length - current_length
                    if remaining_space > 50:  # Only add if meaningful space remains
                        context_parts.append(content[:remaining_space] + "...")
                    break
            
            return " ".join(context_parts)
            
        except Exception as e:
            logger.error(f"Failed to get relevant context: {e}")
            return ""
    
    def initialize_sample_data(self) -> bool:
        """Initialize with sample reflection knowledge"""
        sample_documents = [
            Document(
                page_content="Reflection is the process of looking inward to understand one's thoughts and feelings.",
                metadata={"category": "reflection", "source": "philosophy"}
            ),
            Document(
                page_content="Questions that begin with 'what' or 'how' often encourage deeper reflection than 'why' questions.",
                metadata={"category": "questioning", "source": "psychology"}
            ),
            Document(
                page_content="Non-directive guidance allows individuals to discover their own insights without being told what to do.",
                metadata={"category": "approach", "source": "therapy"}
            ),
            Document(
                page_content="Silence and pause in conversation can create space for reflection and deeper thinking.",
                metadata={"category": "technique", "source": "counseling"}
            ),
            Document(
                page_content="Metaphorical questions can help people see situations from new perspectives.",
                metadata={"category": "technique", "source": "coaching"}
            )
        ]
        
        return self.add_documents(sample_documents)
    
    def clear_store(self) -> bool:
        """Clear all documents from store"""
        try:
            if self.store_type.lower() == "faiss":
                # Recreate empty FAISS index
                self._store = self._create_empty_store()
            else:  # Chroma
                self._store.delete_collection()
                self._store = Chroma(
                    persist_directory=os.path.join(self.store_path, "chroma"),
                    embedding_function=self.embedder.embeddings
                )
            
            logger.info(f"Cleared {self.store_type} store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear store: {e}")
            return False
