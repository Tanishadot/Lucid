from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
from core.utils.logger import logger


@dataclass
class Message:
    """Represents a single message in conversation"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    text: str = ""
    is_user: bool = True
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Session:
    """Represents a conversation session"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    user_context: Dict[str, Any] = field(default_factory=dict)


class MemoryManager:
    """Manages conversation context and short-term memory"""
    
    def __init__(self, max_conversation_length: int = 20, session_timeout_minutes: int = 30):
        self.max_conversation_length = max_conversation_length
        self.session_timeout_minutes = session_timeout_minutes
        self.sessions: Dict[str, Session] = {}
        logger.info(f"MemoryManager initialized with max_length={max_conversation_length}, timeout={session_timeout_minutes}min")
    
    def create_session(self, user_context: Optional[Dict[str, Any]] = None) -> str:
        """Create a new conversation session"""
        session = Session(user_context=user_context or {})
        self.sessions[session.id] = session
        logger.info(f"Created new session: {session.id}")
        return session.id
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID, updating last activity"""
        session = self.sessions.get(session_id)
        if session:
            session.last_activity = datetime.now()
        return session
    
    def add_message(self, session_id: str, message: str, is_user: bool = True, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a message to a session"""
        session = self.get_session(session_id)
        if not session:
            logger.warning(f"Session not found: {session_id}")
            return False
        
        msg = Message(text=message, is_user=is_user, metadata=metadata or {})
        session.messages.append(msg)
        
        # Maintain conversation length limit
        if len(session.messages) > self.max_conversation_length:
            # Remove oldest messages, keeping at least one user message for context
            user_messages = [m for m in session.messages if m.is_user]
            if len(user_messages) > 1:
                # Remove everything up to the second oldest user message
                second_oldest_user_idx = next(i for i, m in enumerate(session.messages) 
                                           if m.is_user and i > 0)
                session.messages = session.messages[second_oldest_user_idx:]
            else:
                # Remove oldest message if only one user message exists
                session.messages.pop(0)
        
        logger.debug(f"Added message to session {session_id}: {'user' if is_user else 'assistant'}")
        return True
    
    def get_conversation_context(self, session_id: str, max_messages: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation context for prompt building"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        messages = session.messages
        if max_messages:
            messages = messages[-max_messages:]
        
        return [
            {
                "text": msg.text,
                "is_user": msg.is_user,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata
            }
            for msg in messages
        ]
    
    def get_recent_user_messages(self, session_id: str, count: int = 3) -> List[str]:
        """Get recent user messages for context"""
        context = self.get_conversation_context(session_id)
        return [msg["text"] for msg in context if msg["is_user"]][-count:]
    
    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions and return count of removed sessions"""
        cutoff_time = datetime.now() - timedelta(minutes=self.session_timeout_minutes)
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if session.last_activity < cutoff_time
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        
        return len(expired_sessions)
    
    def get_session_count(self) -> int:
        """Get total number of active sessions"""
        return len(self.sessions)
    
    def export_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Export session data for analysis"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session.id,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "user_context": session.user_context,
            "messages": [
                {
                    "id": msg.id,
                    "text": msg.text,
                    "is_user": msg.is_user,
                    "timestamp": msg.timestamp.isoformat(),
                    "metadata": msg.metadata
                }
                for msg in session.messages
            ]
        }
    
    def clear_session(self, session_id: str) -> bool:
        """Clear all messages in a session"""
        session = self.get_session(session_id)
        if session:
            session.messages.clear()
            session.last_activity = datetime.now()
            logger.info(f"Cleared session: {session_id}")
            return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session entirely"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
