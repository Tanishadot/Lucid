import re
import os
from typing import Dict, List, Optional
from llm_reflection import LLMReflectionGenerator

class ReflectionEngine:
    def __init__(self):
        self.question_templates = {
            "emotional_clarification": [
                "What emotions are present in this moment?",
                "How does this feeling show up in your body?",
                "What might this emotion be trying to tell you?",
                "What would happen if you sat with this feeling without judgment?",
            ],
            "assumption_exposure": [
                "What assumptions are you making about this situation?",
                "Which of these beliefs might be worth questioning?",
                "What if the opposite of your assumption were true?",
                "What evidence do you have that supports or challenges this belief?",
            ],
            "value_conflict": [
                "What values feel most important to you right now?",
                "Where might your values be in tension with each other?",
                "What would honoring your deepest values look like here?",
                "Which choice aligns more closely with who you want to be?",
            ],
            "perspective_broadening": [
                "How might you see this situation from a different angle?",
                "What advice would you give a friend in this situation?",
                "How might you view this challenge in five years?",
                "What haven't you considered yet?",
            ],
            "pattern_recognition": [
                "What patterns do you notice in your thinking or behavior?",
                "When have you felt this way before?",
                "What might this pattern be protecting you from?",
                "What would it mean to break this pattern?",
            ],
        }
        
        self.cognitive_patterns = {
            "all_or_nothing": ["always", "never", "perfect", "failure"],
            "catastrophizing": ["disaster", "terrible", "awful", "worst"],
            "mind_reading": ["they think", "they must", "probably"],
            "fortune_telling": ["will happen", "going to", "expect"],
        }
        
        self.test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        
        if not self.test_mode:
            self.llm_generator = LLMReflectionGenerator()

    def generate_reflection(self, message: str, session_context: List[Dict]) -> str:
        """Generate reflection using LLM with analysis metadata"""
        if self.test_mode:
            return "What feels most present for you in this moment?"
        
        # Analyze the message to get metadata
        question_type = self._classify_message(message)
        emotion = self._detect_emotion(message)
        cognitive_pattern = self._detect_cognitive_pattern(message)
        value_conflict = self._detect_value_conflict(message)
        philosophical_context = self._retrieve_philosophical_context(message)
        
        # Generate reflection using LLM
        return self.llm_generator.generate_reflection(
            message=message,
            emotion=emotion,
            cognitive_pattern=cognitive_pattern,
            value_conflict=value_conflict,
            question_type=question_type,
            philosophical_context=philosophical_context
        )

    def analyze_message(self, message: str) -> Dict:
        """Generate metadata about the message (internal use only)"""
        emotion = self._detect_emotion(message)
        cognitive_pattern = self._detect_cognitive_pattern(message)
        value_conflict = self._detect_value_conflict(message)
        
        return {
            "emotion": emotion,
            "cognitive_pattern": cognitive_pattern,
            "value_conflict": value_conflict,
        }

    def _retrieve_philosophical_context(self, message: str) -> str:
        """Placeholder for future RAG integration"""
        # TODO: Implement RAG-based philosophical context retrieval
        return ""

    def _classify_message(self, message: str) -> str:
        """Classify the message to determine appropriate question type"""
        message_lower = message.lower()
        
        # Check for emotional content
        if any(word in message_lower for word in ["feel", "feeling", "emotion", "sad", "happy", "angry", "anxious"]):
            return "emotional_clarification"
        
        # Check for assumptions
        if any(word in message_lower for word in ["assume", "belief", "think", "should", "must"]):
            return "assumption_exposure"
        
        # Check for decision/conflict
        if any(word in message_lower for word in ["choose", "decision", "conflict", "between", "either"]):
            return "value_conflict"
        
        # Check for stuck patterns
        if any(word in message_lower for word in ["stuck", "pattern", "always", "never", "repeat"]):
            return "pattern_recognition"
        
        # Default to perspective broadening
        return "perspective_broadening"

    def _detect_emotion(self, message: str) -> str:
        """Simple emotion detection"""
        emotions = {
            "anxiety": ["anxious", "worried", "nervous", "panic"],
            "sadness": ["sad", "depressed", "unhappy", "down"],
            "anger": ["angry", "frustrated", "irritated", "mad"],
            "joy": ["happy", "excited", "glad", "pleased"],
            "confusion": ["confused", "uncertain", "unsure", "unclear"],
        }
        
        message_lower = message.lower()
        for emotion, keywords in emotions.items():
            if any(keyword in message_lower for keyword in keywords):
                return emotion
        return "neutral"

    def _detect_cognitive_pattern(self, message: str) -> str:
        """Detect cognitive distortions"""
        message_lower = message.lower()
        
        for pattern, keywords in self.cognitive_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return pattern
        return "balanced"

    def _detect_value_conflict(self, message: str) -> str:
        """Detect potential value conflicts"""
        values = {
            "security_vs_freedom": ["safe", "secure", "stable", "free", "adventure", "risk"],
            "individual_vs_relationship": ["me", "myself", "others", "relationship", "connection"],
            "growth_vs_comfort": ["comfortable", "easy", "challenge", "grow", "learn"],
        }
        
        message_lower = message.lower()
        for conflict, keywords in values.items():
            found_values = [kw for kw in keywords if kw in message_lower]
            if len(found_values) > 1:
                return conflict
        return "none"

    def _avoid_repetition(self, templates: List[str], session_context: List[Dict]) -> List[str]:
        """Avoid repeating questions used recently"""
        if not session_context:
            return templates
        
        recent_messages = [msg["text"] for msg in session_context[-5:]]  # Last 5 messages
        recent_text = " ".join(recent_messages).lower()
        
        available = []
        for template in templates:
            template_lower = template.lower()
            # Check if any significant words from template appear in recent messages
            template_words = set(re.findall(r'\b\w+\b', template_lower))
            recent_words = set(re.findall(r'\b\w+\b', recent_text))
            
            # If less than 30% of template words appear in recent messages, it's available
            overlap = len(template_words & recent_words) / len(template_words) if template_words else 0
            if overlap < 0.3:
                available.append(template)
        
        return available if available else templates
