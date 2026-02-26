from typing import Dict, Any, Optional
from pydantic import BaseModel
from core.reflection_engine.engine import ReflectionEngine
from core.memory.memory_manager import MemoryManager
from core.constraint_validator.validator import ConstraintValidator
from core.utils.logger import logger
from config.settings import settings


class ChatRequest(BaseModel):
    """Request model for chat interactions"""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat interactions"""
    response: str
    session_id: str
    success: bool
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SessionInfo(BaseModel):
    """Session information model"""
    session_id: str
    message_count: int
    created_at: str
    last_activity: str


class ChatService:
    """Orchestrates the complete reflection pipeline"""
    
    def __init__(self):
        self.reflection_engine = ReflectionEngine()
        self.memory_manager = MemoryManager(
            max_conversation_length=settings.max_conversation_length,
            session_timeout_minutes=settings.session_timeout_minutes
        )
        self.constraint_validator = ConstraintValidator()
        
        logger.info("ChatService initialized")
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Process a chat request through the complete pipeline"""
        try:
            # Step 1: Validate input
            input_validation = self.constraint_validator.validate_input(request.message)
            if not input_validation.is_valid:
                return ChatResponse(
                    response="",
                    session_id=request.session_id or "",
                    success=False,
                    error=f"Invalid input: {', '.join(input_validation.violations)}"
                )
            
            # Step 2: Get or create session
            session_id = request.session_id
            if not session_id or not self.memory_manager.get_session(session_id):
                session_id = self.memory_manager.create_session()
                logger.info(f"Created new session: {session_id}")
            
            # Step 3: Generate reflection
            reflection_result = self.reflection_engine.generate_reflection(
                session_id=session_id,
                user_message=request.message
            )
            
            if not reflection_result["success"]:
                return ChatResponse(
                    response="",
                    session_id=session_id,
                    success=False,
                    error=reflection_result.get("error", "Reflection generation failed")
                )
            
            # Step 4: Build response
            response = ChatResponse(
                response=reflection_result["response"],
                session_id=session_id,
                success=True,
                metadata=reflection_result.get("metadata", {})
            )
            
            logger.info(f"Chat completed successfully for session {session_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error in chat service: {e}")
            return ChatResponse(
                response="",
                session_id=request.session_id or "",
                success=False,
                error="Service temporarily unavailable"
            )
    
    async def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
        """Get information about a session"""
        try:
            session = self.memory_manager.get_session(session_id)
            if not session:
                return None
            
            return SessionInfo(
                session_id=session.id,
                message_count=len(session.messages),
                created_at=session.created_at.isoformat(),
                last_activity=session.last_activity.isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error getting session info: {e}")
            return None
    
    async def get_conversation_history(self, session_id: str, max_messages: int = 10) -> list:
        """Get conversation history for a session"""
        try:
            context = self.memory_manager.get_conversation_context(session_id, max_messages)
            return context[-max_messages:]  # Return most recent messages
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    async def clear_session(self, session_id: str) -> bool:
        """Clear conversation history for a session"""
        try:
            success = self.memory_manager.clear_session(session_id)
            if success:
                logger.info(f"Cleared session: {session_id}")
            return success
            
        except Exception as e:
            logger.error(f"Error clearing session: {e}")
            return False
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session entirely"""
        try:
            success = self.memory_manager.delete_session(session_id)
            if success:
                logger.info(f"Deleted session: {session_id}")
            return success
            
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False
    
    async def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        try:
            # Cleanup expired sessions first
            cleaned_count = self.memory_manager.cleanup_expired_sessions()
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} expired sessions")
            
            return self.memory_manager.get_session_count()
            
        except Exception as e:
            logger.error(f"Error getting active sessions count: {e}")
            return 0
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all components"""
        try:
            health_status = {
                "status": "healthy",
                "components": {},
                "settings": {
                    "test_mode": settings.test_mode,
                    "llm_model": settings.openai_model,
                    "vector_store_type": settings.vector_store_type
                }
            }
            
            # Check reflection engine
            try:
                # Simple test reflection
                test_session = self.memory_manager.create_session()
                test_result = self.reflection_engine.generate_reflection(
                    session_id=test_session,
                    user_message="Hello"
                )
                health_status["components"]["reflection_engine"] = {
                    "status": "healthy" if test_result["success"] else "unhealthy",
                    "details": test_result.get("metadata", {})
                }
                # Cleanup test session
                self.memory_manager.delete_session(test_session)
            except Exception as e:
                health_status["components"]["reflection_engine"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
            
            # Check memory manager
            try:
                session_count = self.memory_manager.get_session_count()
                health_status["components"]["memory_manager"] = {
                    "status": "healthy",
                    "active_sessions": session_count
                }
            except Exception as e:
                health_status["components"]["memory_manager"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
            
            # Check constraint validator
            try:
                test_validation = self.constraint_validator.validate_output("What feels unclear right now?")
                health_status["components"]["constraint_validator"] = {
                    "status": "healthy" if test_validation.is_valid else "unhealthy",
                    "test_validation": test_validation.__dict__
                }
            except Exception as e:
                health_status["components"]["constraint_validator"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
            
            # Overall status
            all_healthy = all(
                component["status"] == "healthy" 
                for component in health_status["components"].values()
            )
            health_status["status"] = "healthy" if all_healthy else "degraded"
            
            return health_status
            
        except Exception as e:
            logger.error(f"Error in health check: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def analyze_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Analyze session for insights"""
        try:
            summary = self.reflection_engine.get_session_summary(session_id)
            if not summary:
                return None
            
            # Add additional analytics
            session = self.memory_manager.get_session(session_id)
            if session:
                summary["analytics"] = {
                    "average_message_length": sum(len(msg.text) for msg in session.messages) / len(session.messages) if session.messages else 0,
                    "user_to_lucid_ratio": len([m for m in session.messages if m.is_user]) / len([m for m in session.messages if not m.is_user]) if len([m for m in session.messages if not m.is_user]) > 0 else 0,
                    "session_duration_minutes": (session.last_activity - session.created_at).total_seconds() / 60
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error analyzing session: {e}")
            return None
