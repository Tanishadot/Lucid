from typing import List, Optional
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from config.settings import settings
from core.utils.logger import logger


class Embedder:
    """Handles text embeddings for knowledge retrieval"""
    
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.embedding_model
        self._embeddings = None
        logger.info(f"Embedder initialized with model: {self.model_name}")
    
    @property
    def embeddings(self):
        """Lazy initialization of embeddings"""
        if self._embeddings is None:
            try:
                self._embeddings = OpenAIEmbeddings(
                    model=self.model_name,
                    openai_api_key=settings.openai_api_key
                )
                logger.info("OpenAI embeddings initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI embeddings: {e}")
                # Fallback to dummy embeddings for testing
                self._embeddings = DummyEmbeddings()
                logger.warning("Using dummy embeddings for testing")
        
        return self._embeddings
    
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text"""
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            logger.error(f"Failed to embed text: {e}")
            return [0.0] * 1536  # Default embedding dimension
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts"""
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            logger.error(f"Failed to embed texts: {e}")
            return [[0.0] * 1536 for _ in texts]  # Default embedding dimension
    
    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """Embed documents with metadata"""
        texts = [doc.page_content for doc in documents]
        return self.embed_texts(texts)


class DummyEmbeddings:
    """Dummy embeddings for testing when OpenAI is unavailable"""
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
    
    def embed_query(self, text: str) -> List[float]:
        """Generate dummy embedding for query"""
        # Simple hash-based deterministic embedding
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Convert hash to float values
        embedding = []
        for i in range(0, len(hash_hex), 2):
            hex_pair = hash_hex[i:i+2]
            val = int(hex_pair, 16) / 255.0
            embedding.append(val)
        
        # Pad or truncate to desired dimension
        while len(embedding) < self.dimension:
            embedding.append(0.0)
        
        return embedding[:self.dimension]
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate dummy embeddings for documents"""
        return [self.embed_query(text) for text in texts]
