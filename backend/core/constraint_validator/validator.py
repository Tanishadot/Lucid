from typing import List, Dict, Any
from .rules import ConstraintRules, ValidationResult, ValidationRule
from core.utils.logger import logger


class ConstraintValidator:
    """Validates LUCID constraints for inputs and outputs"""
    
    def __init__(self):
        self.rules = ConstraintRules()
        logger.info("ConstraintValidator initialized")
    
    def validate_input(self, user_message: str) -> ValidationResult:
        """Validate user input for safety and appropriateness"""
        violations = []
        
        # Basic input validation
        if not user_message or not user_message.strip():
            violations.append("Empty message")
        
        if len(user_message) > 1000:
            violations.append("Message too long")
        
        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            confidence=1.0 if len(violations) == 0 else 0.5
        )
    
    def validate_output(self, llm_response: str) -> ValidationResult:
        """Validate LLM response against LUCID constraints"""
        all_violations = []
        confidences = []
        
        # Run all constraint validations
        validations = [
            self.rules.validate_no_directive(llm_response),
            self.rules.validate_single_question(llm_response),
            self.rules.validate_reflective_only(llm_response),
            self.rules.validate_max_length(llm_response)
        ]
        
        for validation in validations:
            all_violations.extend(validation.violations)
            confidences.append(validation.confidence)
        
        # Calculate overall confidence
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Log violations if any
        if all_violations:
            logger.warning(f"Constraint violations: {all_violations}")
        
        return ValidationResult(
            is_valid=len(all_violations) == 0,
            violations=all_violations,
            confidence=overall_confidence
        )
    
    def validate_all_constraints(self, user_message: str, llm_response: str) -> Dict[str, ValidationResult]:
        """Validate both input and output"""
        return {
            "input": self.validate_input(user_message),
            "output": self.validate_output(llm_response)
        }
    
    def is_response_acceptable(self, llm_response: str, min_confidence: float = 0.8) -> bool:
        """Quick check if response meets minimum acceptance criteria"""
        validation = self.validate_output(llm_response)
        return validation.is_valid and validation.confidence >= min_confidence
