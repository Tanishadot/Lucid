from functools import lru_cache
from services.chat_service import ChatService
from core.utils.logger import logger


@lru_cache()
def get_chat_service() -> ChatService:
    """Dependency for ChatService - cached for performance"""
    try:
        service = ChatService()
        logger.info("ChatService dependency created")
        return service
    except Exception as e:
        logger.error(f"Failed to create ChatService dependency: {e}")
        raise
