import re
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class SafetyResult:
    requires_redirection: bool
    redirect_response: str
    risk_level: str

class SafetyLayer:
    def __init__(self):
        self.adice_keywords = [
            "should", "must", "have to", "need to", "tell me", "give me", "what should",
            "how should", "recommend", "suggest", "advice", "instruction", "steps",
            "tell me what to do", "help me decide", "make decision for me"
        ]
        
        self.dependency_patterns = [
            r"i can't.*without you",
            r"i need you to.*",
            r"please tell me.*",
            r"just tell me.*",
            r"i don't know.*help me",
        ]
        
        self.distress_keywords = [
            "suicide", "kill myself", "end my life", "want to die",
            "self harm", "hurt myself", "can't go on", "no reason to live",
            "better off dead", "want to disappear"
        ]
        
        self.high_distress_indicators = [
            "crisis", "emergency", "urgent", "can't cope", "overwhelmed",
            "breaking point", "at my limit", "can't take it anymore"
        ]

    def check_message(self, message: str) -> SafetyResult:
        """Check message for safety concerns and determine if redirection is needed"""
        message_lower = message.lower()
        
        # Check for immediate safety concerns
        if self._check_immediate_safety(message_lower):
            return SafetyResult(
                requires_redirection=True,
                redirect_response=self._get_safety_redirect(),
                risk_level="high"
            )
        
        # Check for high distress
        if self._check_high_distress(message_lower):
            return SafetyResult(
                requires_redirection=True,
                redirect_response=self._get_distress_redirect(),
                risk_level="medium"
            )
        
        # Check for advice-seeking behavior
        if self._check_advice_seeking(message_lower):
            return SafetyResult(
                requires_redirection=True,
                redirect_response=self._get_reflection_redirect(),
                risk_level="low"
            )
        
        # Check for dependency language
        if self._check_dependency(message_lower):
            return SafetyResult(
                requires_redirection=True,
                redirect_response=self._get_autonomy_redirect(),
                risk_level="low"
            )
        
        return SafetyResult(
            requires_redirection=False,
            redirect_response="",
            risk_level="safe"
        )

    def _check_immediate_safety(self, message: str) -> bool:
        """Check for immediate safety concerns"""
        return any(keyword in message for keyword in self.distress_keywords)

    def _check_high_distress(self, message: str) -> bool:
        """Check for high emotional distress"""
        return any(keyword in message for keyword in self.high_distress_indicators)

    def _check_advice_seeking(self, message: str) -> bool:
        """Check if user is seeking direct advice"""
        # Check for advice keywords
        if any(keyword in message for keyword in self.advice_keywords):
            return True
        
        # Check for dependency patterns
        for pattern in self.dependency_patterns:
            if re.search(pattern, message):
                return True
        
        return False

    def _check_dependency(self, message: str) -> bool:
        """Check for dependency language"""
        dependency_indicators = [
            "i can't decide",
            "i don't know what to do",
            "i'm lost",
            "i'm confused",
            "i need help deciding",
        ]
        
        return any(indicator in message for indicator in dependency_indicators)

    def _get_safety_redirect(self) -> str:
        """Get response for immediate safety concerns"""
        return "I hear that you're going through something really difficult. Your wellbeing matters deeply. Consider reaching out to a mental health professional or crisis support line. You deserve support from someone who can help you through this."

    def _get_distress_redirect(self) -> str:
        """Get response for high emotional distress"""
        return "It sounds like you're carrying a heavy weight right now. What would it mean to give yourself permission to seek support from someone who can walk alongside you through this?"

    def _get_reflection_redirect(self) -> str:
        """Get response for advice-seeking behavior"""
        reflection_redirects = [
            "What wisdom might already be within you about this situation?",
            "If you trusted your own knowing, what might you discover?",
            "What would you tell a friend who came to you with this same question?",
            "What feels most true for you when you set aside what you think you should do?",
        ]
        
        import random
        return random.choice(reflection_redirects)

    def _get_autonomy_redirect(self) -> str:
        """Get response for dependency language"""
        autonomy_redirects = [
            "What feels most unclear about this situation for you?",
            "What part of this decision feels most challenging right now?",
            "What would exploring this question look like for you?",
            "What inner resources might you draw upon in this moment?",
        ]
        
        import random
        return random.choice(autonomy_redirects)
