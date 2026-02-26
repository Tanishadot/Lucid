from typing import Dict, List, Any, Optional
from enum import Enum
from core.utils.logger import logger


class QuestionStrategy(Enum):
    """Types of questioning strategies for reflection"""
    CLARIFICATION = "clarification"
    PERSPECTIVE_SHIFT = "perspective_shift"
    EXPLORATION = "exploration"
    VALUES_INQUIRY = "values_inquiry"
    FUTURE_ORIENTED = "future_oriented"
    SENSORY_FOCUS = "sensory_focus"


class QuestioningStrategies:
    """Collection of questioning strategies for different reflection contexts"""
    
    def __init__(self):
        self.strategy_templates = self._initialize_templates()
        logger.info("QuestioningStrategies initialized")
    
    def _initialize_templates(self) -> Dict[QuestionStrategy, List[str]]:
        """Initialize question templates for each strategy"""
        return {
            QuestionStrategy.CLARIFICATION: [
                "What feels unclear about this situation?",
                "What part of this seems most confusing?",
                "What would help you understand this better?",
                "What details feel missing from your understanding?",
                "What assumptions are you making about this?"
            ],
            QuestionStrategy.PERSPECTIVE_SHIFT: [
                "How might this look from a different angle?",
                "What would someone else notice about this?",
                "If you could change one thing about your view, what would it be?",
                "What haven't you considered yet?",
                "How might this seem different tomorrow?"
            ],
            QuestionStrategy.EXPLORATION: [
                "What possibilities are you not seeing?",
                "What would you explore if there were no limits?",
                "What paths forward feel worth investigating?",
                "What new directions might emerge from this?",
                "What would happen if you followed your curiosity?"
            ],
            QuestionStrategy.VALUES_INQUIRY: [
                "What matters most to you in this moment?",
                "What values are at play here?",
                "What would feel most aligned with who you are?",
                "What choice would honor what's important to you?",
                "What feels truest to you right now?"
            ],
            QuestionStrategy.FUTURE_ORIENTED: [
                "What might become possible from here?",
                "What next step feels worth considering?",
                "How could this evolve over time?",
                "What future are you imagining?",
                "What would you like to see emerge?"
            ],
            QuestionStrategy.SENSORY_FOCUS: [
                "What do you notice in your body right now?",
                "What sensations are present?",
                "What does this feel like physically?",
                "What are you experiencing in this moment?",
                "What do you sense beneath the surface?"
            ]
        }
    
    def select_strategy(self, context: Dict[str, Any]) -> QuestionStrategy:
        """Select appropriate questioning strategy based on context"""
        emotions = context.get("emotions", [])
        patterns = context.get("cognitive_patterns", [])
        user_message = context.get("user_message", "").lower()
        
        # Strategy selection logic
        if any(emotion in emotions for emotion in ["confusion", "uncertainty"]):
            return QuestionStrategy.CLARIFICATION
        elif any(emotion in emotions for emotion in ["frustration", "stuck"]):
            return QuestionStrategy.PERSPECTIVE_SHIFT
        elif any(emotion in emotions for emotion in ["curiosity", "exploration"]):
            return QuestionStrategy.EXPLORATION
        elif any(pattern in patterns for pattern in ["values_conflict", "decision_making"]):
            return QuestionStrategy.VALUES_INQUIRY
        elif any(word in user_message for word in ["future", "next", "goal", "plan"]):
            return QuestionStrategy.FUTURE_ORIENTED
        elif any(word in user_message for word in ["feel", "body", "sensation", "physical"]):
            return QuestionStrategy.SENSORY_FOCUS
        else:
            return QuestionStrategy.EXPLORATION  # Default strategy
    
    def get_template_for_strategy(self, strategy: QuestionStrategy) -> List[str]:
        """Get question templates for a specific strategy"""
        return self.strategy_templates.get(strategy, self.strategy_templates[QuestionStrategy.EXPLORATION])
    
    def adapt_template_to_context(self, template: str, context: Dict[str, Any]) -> str:
        """Adapt a question template to specific context"""
        # Simple adaptation - can be enhanced with more sophisticated logic
        adapted = template
        
        # Add context-specific modifications
        if "repetition" in context.get("cognitive_patterns", []):
            adapted = adapted.replace("What", "What new")
        
        if "overwhelm" in context.get("emotions", []):
            adapted = adapted.replace("What", "What one")
        
        return adapted
    
    def generate_strategy_question(self, context: Dict[str, Any]) -> str:
        """Generate a question using strategy-based approach"""
        strategy = self.select_strategy(context)
        templates = self.get_template_for_strategy(strategy)
        
        # Select template (can be enhanced with better selection logic)
        import random
        selected_template = random.choice(templates)
        
        # Adapt to context
        adapted_template = self.adapt_template_to_context(selected_template, context)
        
        logger.debug(f"Generated {strategy.value} question: {adapted_template}")
        return adapted_template
    
    def get_all_strategies(self) -> List[QuestionStrategy]:
        """Get all available questioning strategies"""
        return list(QuestionStrategy)
    
    def get_strategy_description(self, strategy: QuestionStrategy) -> str:
        """Get description of a questioning strategy"""
        descriptions = {
            QuestionStrategy.CLARIFICATION: "Helps clarify confusion and uncertainty",
            QuestionStrategy.PERSPECTIVE_SHIFT: "Encourages viewing situations from new angles",
            QuestionStrategy.EXPLORATION: "Opens up possibilities and new directions",
            QuestionStrategy.VALUES_INQUIRY: "Focuses on what matters most to the person",
            QuestionStrategy.FUTURE_ORIENTED: "Points toward future possibilities",
            QuestionStrategy.SENSORY_FOCUS: "Brings attention to present-moment experience"
        }
        return descriptions.get(strategy, "Unknown strategy")
    
    def validate_strategy_question(self, question: str, strategy: QuestionStrategy) -> bool:
        """Validate that a question fits the intended strategy"""
        templates = self.get_template_for_strategy(strategy)
        
        # Check if question structure matches template patterns
        for template in templates:
            # Simple pattern matching - can be enhanced
            if question.startswith(template.split("?")[0].split(",")[0]):
                return True
        
        return False
