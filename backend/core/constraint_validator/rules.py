from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ValidationRule(Enum):
    """Types of validation rules for LUCID constraints"""
    NO_DIRECTIVE = "no_directive"
    SINGLE_QUESTION = "single_question"
    REFLECTIVE_ONLY = "reflective_only"
    NO_ADVICE = "no_advice"
    MAX_LENGTH = "max_length"


@dataclass
class ValidationResult:
    """Result of constraint validation"""
    is_valid: bool
    violations: List[str]
    confidence: float = 1.0


class ConstraintRules:
    """LUCID philosophical constraint rules"""
    
    # Forbidden patterns that violate non-directive principle
    DIRECTIVE_PATTERNS = [
        "you should", "you must", "you need to", "you have to",
        "i suggest", "i recommend", "i advise", "let me tell you",
        "the best way", "you ought to", "it would be better if"
    ]
    
    # Question patterns (allowed)
    QUESTION_MARKERS = ["?", "what", "how", "when", "where", "why", "which"]
    
    # Advice patterns (forbidden)
    ADVICE_PATTERNS = [
        "try to", "consider", "think about", "you could",
        "perhaps you", "maybe you", "have you thought about"
    ]
    
    @classmethod
    def validate_no_directive(cls, text: str) -> ValidationResult:
        """Validate that text contains no directive language"""
        violations = []
        text_lower = text.lower()
        
        for pattern in cls.DIRECTIVE_PATTERNS:
            if pattern in text_lower:
                violations.append(f"Directive language detected: '{pattern}'")
        
        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            confidence=1.0 - (len(violations) * 0.2)
        )
    
    @classmethod
    def validate_single_question(cls, text: str) -> ValidationResult:
        """Validate that text contains exactly one question"""
        question_count = text.count('?')
        violations = []
        
        if question_count == 0:
            violations.append("No question found")
        elif question_count > 1:
            violations.append(f"Multiple questions found: {question_count}")
        
        return ValidationResult(
            is_valid=question_count == 1,
            violations=violations,
            confidence=1.0 if question_count == 1 else 0.5
        )
    
    @classmethod
    def validate_reflective_only(cls, text: str) -> ValidationResult:
        """Validate that text is purely reflective"""
        violations = []
        text_lower = text.lower()
        
        # Check for advice patterns
        for pattern in cls.ADVICE_PATTERNS:
            if pattern in text_lower:
                violations.append(f"Advice pattern detected: '{pattern}'")
        
        # Check for statements instead of questions
        if '?' not in text and any(marker in text_lower for marker in ["i think", "i believe", "i feel"]):
            violations.append("Statement instead of reflective question")
        
        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            confidence=1.0 - (len(violations) * 0.15)
        )
    
    @classmethod
    def validate_max_length(cls, text: str, max_length: int = 150) -> ValidationResult:
        """Validate maximum response length"""
        violations = []
        
        if len(text) > max_length:
            violations.append(f"Response too long: {len(text)} > {max_length}")
        
        return ValidationResult(
            is_valid=len(text) <= max_length,
            violations=violations,
            confidence=1.0 if len(text) <= max_length else 0.7
        )
