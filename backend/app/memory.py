from typing import Dict, List, Optional
from datetime import datetime
import json

class MemoryManager:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
        self.max_messages_per_session = 100  # Limit session size

    def create_session(self, session_id: str) -> None:
        """Create a new session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def add_message(self, session_id: str, message: str, is_user: bool) -> None:
        """Add a message to the session"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        message_data = {
            "text": message,
            "is_user": is_user,
            "timestamp": datetime.now().isoformat(),
            "id": len(self.sessions[session_id]) + 1
        }
        
        self.sessions[session_id].append(message_data)
        
        # Limit session size
        if len(self.sessions[session_id]) > self.max_messages_per_session:
            self.sessions[session_id] = self.sessions[session_id][-self.max_messages_per_session:]

    def get_session_context(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get recent messages from session for context"""
        if session_id not in self.sessions:
            return []
        
        return self.sessions[session_id][-limit:]

    def get_full_session(self, session_id: str) -> List[Dict]:
        """Get all messages from session"""
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str) -> None:
        """Clear all messages from session"""
        if session_id in self.sessions:
            self.sessions[session_id] = []

    def delete_session(self, session_id: str) -> None:
        """Delete a session entirely"""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_session_summary(self, session_id: str) -> Dict:
        """Get summary information about a session"""
        if session_id not in self.sessions:
            return {"exists": False}
        
        messages = self.sessions[session_id]
        user_messages = [msg for msg in messages if msg["is_user"]]
        ai_messages = [msg for msg in messages if not msg["is_user"]]
        
        return {
            "exists": True,
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "ai_messages": len(ai_messages),
            "last_activity": messages[-1]["timestamp"] if messages else None,
            "created": messages[0]["timestamp"] if messages else None
        }

    def search_sessions(self, query: str, limit: int = 5) -> List[Dict]:
        """Search through sessions for specific content"""
        results = []
        query_lower = query.lower()
        
        for session_id, messages in self.sessions.items():
            for message in messages:
                if query_lower in message["text"].lower():
                    results.append({
                        "session_id": session_id,
                        "message": message,
                        "context": self.get_session_context(session_id, 3)
                    })
                    if len(results) >= limit:
                        return results
        
        return results

    def export_session(self, session_id: str) -> Optional[str]:
        """Export session as JSON string"""
        if session_id not in self.sessions:
            return None
        
        session_data = {
            "session_id": session_id,
            "messages": self.sessions[session_id],
            "exported_at": datetime.now().isoformat()
        }
        
        return json.dumps(session_data, indent=2)

    def get_all_session_ids(self) -> List[str]:
        """Get list of all session IDs"""
        return list(self.sessions.keys())

    def get_session_count(self) -> int:
        """Get total number of sessions"""
        return len(self.sessions)
