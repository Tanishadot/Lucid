from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from core.utils.logger import logger


@dataclass
class PromptContext:
    """Context data for prompt building"""
    user_message: str
    conversation_history: List[Dict[str, Any]]
    philosophical_context: str
    emotion_indicators: List[str]
    cognitive_patterns: List[str]
    session_metadata: Dict[str, Any]


class PromptBuilder:
    """Builds structured prompts for LUCID reflection generation"""
    
    def __init__(self):
        self.system_prompt = self._get_system_prompt()
        self.reflection_guidelines = self._get_reflection_guidelines()
        logger.info("PromptBuilder initialized")
    
    def build_reflection_prompt(self, context: PromptContext) -> str:
        """Build complete prompt for reflection generation"""
        prompt_parts = [
            self.system_prompt,
            self._build_context_section(context),
            self.reflection_guidelines,
            self._build_task_instruction(context)
        ]
        
        return "\n\n".join(prompt_parts)
    
    def _get_system_prompt(self) -> str:
        """Core system prompt defining LUCID's role"""
        return """You are LUCID, a reflective AI companion designed to help people explore their thoughts and feelings through gentle, non-directive questioning.

Your core purpose is to facilitate self-discovery by asking thoughtful, open-ended questions that encourage deeper reflection. You never give advice, instructions, or direct guidance. Instead, you create space for the person to find their own insights.

Every response must be exactly ONE question that:
- Encourages reflection without suggesting answers
- Avoids directive language ("you should", "try to", etc.)
- Is open-ended and thought-provoking
- Is under 150 characters
- Maintains a supportive, curious tone"""
    
    def _get_reflection_guidelines(self) -> str:
        """Specific guidelines for question generation"""
        return """GUIDELINES:
✓ Ask "what" or "how" questions rather than "why"
✓ Focus on present experience and future possibilities
✓ Use gentle, curious language
✓ Invite exploration without directing
✓ Keep questions concise and clear

AVOID:
✗ Direct advice or instructions
✗ "You should" or "you must" statements
✗ Suggesting specific actions
✗ Multiple questions in one response
✗ Judgmental or interpretive language"""
    
    def _build_context_section(self, context: PromptContext) -> str:
        """Build context section from conversation data"""
        context_parts = []
        
        # Current message
        context_parts.append(f"CURRENT MESSAGE: {context.user_message}")
        
        # Conversation history (recent)
        if context.conversation_history:
            recent_history = context.conversation_history[-3:]  # Last 3 exchanges
            history_text = "\n".join([
                f"{'User' if msg['is_user'] else 'LUCID'}: {msg['text']}"
                for msg in recent_history
            ])
            context_parts.append(f"RECENT CONVERSATION:\n{history_text}")
        
        # Emotional context
        if context.emotion_indicators:
            emotions_text = ", ".join(context.emotion_indicators)
            context_parts.append(f"EMOTIONAL INDICATORS: {emotions_text}")
        
        # Cognitive patterns
        if context.cognitive_patterns:
            patterns_text = ", ".join(context.cognitive_patterns)
            context_parts.append(f"COGNITIVE PATTERNS: {patterns_text}")
        
        # Philosophical context
        if context.philosophical_context:
            context_parts.append(f"PHILOSOPHICAL CONTEXT: {context.philosophical_context}")
        
        return "\n".join(context_parts)
    
    def _build_task_instruction(self, context: PromptContext) -> str:
        """Build specific task instruction"""
        instruction = "Based on the context above, generate exactly ONE reflective question that:"
        
        # Add specific focus based on context
        if "confusion" in context.emotion_indicators or "uncertainty" in context.emotion_indicators:
            instruction += "\n- Helps clarify what feels unclear"
        elif "frustration" in context.emotion_indicators or "stuck" in context.emotion_indicators:
            instruction += "\n- Opens up new perspectives"
        elif "curiosity" in context.emotion_indicators or "exploration" in context.cognitive_patterns:
            instruction += "\n- Encourages deeper exploration"
        else:
            instruction += "\n- Invites gentle reflection"
        
        instruction += "\n\nGenerate your response:"
        return instruction
    
    def build_test_prompt(self, user_message: str) -> str:
        """Build simplified prompt for test mode"""
        return f"""You are LUCID, a reflective AI companion.

User says: "{user_message}"

Generate exactly ONE reflective question (under 150 characters) that encourages deeper reflection without giving advice.

Response:"""
    
    def extract_metadata_for_context(self, conversation_history: List[Dict[str, Any]]) -> PromptContext:
        """Extract relevant metadata from conversation for prompt building"""
        # Get recent user messages for analysis
        recent_user_messages = [
            msg["text"] for msg in conversation_history[-5:] 
            if msg["is_user"]
        ]
        
        # Simple emotion detection (can be enhanced)
        emotion_keywords = {
            "confusion": ["confused", "unclear", "don't know", "unsure"],
            "frustration": ["frustrated", "stuck", "annoyed", "difficult"],
            "curiosity": ["curious", "interested", "wonder", "explore"],
            "uncertainty": ["uncertain", "maybe", "perhaps", "not sure"],
            "reflection": ["think", "feel", "believe", "consider"]
        }
        
        detected_emotions = []
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in " ".join(recent_user_messages).lower() for keyword in keywords):
                detected_emotions.append(emotion)
        
        # Simple cognitive pattern detection
        cognitive_patterns = []
        if any(word in " ".join(recent_user_messages).lower() for word in ["pattern", "always", "never"]):
            cognitive_patterns.append("pattern_recognition")
        if any(word in " ".join(recent_user_messages).lower() for word in ["should", "must", "need"]):
            cognitive_patterns.append("obligation_thinking")
        if any(word in " ".join(recent_user_messages).lower() for word in ["if only", "wish", "hope"]):
            cognitive_patterns.append("hypothetical_thinking")
        
        return PromptContext(
            user_message=recent_user_messages[-1] if recent_user_messages else "",
            conversation_history=conversation_history,
            philosophical_context="",  # Will be filled by knowledge retrieval
            emotion_indicators=detected_emotions,
            cognitive_patterns=cognitive_patterns,
            session_metadata={}
        )
    
    def validate_prompt_completeness(self, prompt: str) -> bool:
        """Validate that prompt contains all necessary components"""
        required_sections = [
            "LUCID", "CURRENT MESSAGE", "GUIDELINES"
        ]
        
        return all(section in prompt for section in required_sections)
