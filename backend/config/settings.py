from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # API Configuration
    app_name: str = "LUCID"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # LLM Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.6
    openai_max_tokens: int = 150
    
    # Vector Store Configuration
    vector_store_type: str = "faiss"  # faiss or chroma
    vector_store_path: str = "data/vector_store"
    embedding_model: str = "text-embedding-3-small"
    
    # Memory Configuration
    max_conversation_length: int = 20
    session_timeout_minutes: int = 30
    
    # Test Mode
    test_mode: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
