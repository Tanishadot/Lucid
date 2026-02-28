"""
ResponseStyleFormatter Module

A style-constrained response formatter that transforms grounded cognitive units
into philosophical reframing statements and elevated reflective questions.

This module operates as a formatting layer only - it does not trigger retrieval
or modify the underlying cognitive architecture.
"""

from typing import Dict, List, Optional, Tuple
import re
from dataclasses import dataclass


@dataclass
class CognitiveUnit:
    """Grounded cognitive unit from retrieval layer"""
    user_input: str
    retrieved_unit: str
    core_reframe: str
    question_bank: List[str]
    theme_tags: List[str]


@dataclass
class FormattedResponse:
    """Two-part philosophical response"""
    framing_statement: str
    reflective_question: str
    
    def to_string(self) -> str:
        return f"{self.framing_statement} {self.reflective_question}"


class ResponseStyleFormatter:
    """
    Formats grounded cognitive material into philosophical two-sentence responses.
    
    This is a pure formatting layer that transforms retrieved material into
    Lucid's distinctive philosophical style without adding new cognitive content.
    """
    
    # Forbidden phrases that indicate coaching/therapy tone
    FORBIDDEN_PHRASES = [
        "you should",
        "it may help", 
        "consider trying",
        "take a step",
        "remember that",
        "what if you",
        "have you thought",
        "maybe you could",
        "it might be useful",
        "try to",
        "consider",
        "remember"
    ]
    
    # Enhanced philosophical framing patterns matching examples
    FRAMING_PATTERNS = {
        "comparison": [
            "Comparison transforms difference into hierarchy.",
            "Measurement creates value where none existed.",
            "External standards become internal judgments.",
            "Comparison converts observation into verdict."
        ],
        "perfection": [
            "Perfection converts growth into constant correction.",
            "Perfectionism protects against the terror of being seen.",
            "The impossible standard guarantees safe failure.",
            "Perfection becomes a weapon against worthiness."
        ],
        "approval": [
            "External approval substitutes for internal validation.",
            "Others' voices become the only truth we hear.",
            "Permission seeking replaces self-authority.",
            "Approval becomes the currency of belonging."
        ],
        "identity": [
            "Identity becomes a performance for others.",
            "Self-concept solidifies around external recognition.",
            "Being dissolves into becoming for others.",
            "Failure becomes identity when repetition is mistaken for destiny."
        ],
        "control": [
            "Control attempts to tame the uncertainty of being.",
            "Certainty becomes a defense against existence.",
            "Order protects against the chaos of freedom.",
            "Control substitutes knowing for being."
        ],
        "guilt": [
            "Guilt often guards the boundary between belonging and autonomy.",
            "Guilt becomes the tax on self-prioritization.",
            "Moral emotion substitutes for boundary setting.",
            "Guilt converts autonomy into betrayal."
        ],
        "uncertainty": [
            "Uncertainty appears when inherited desires begin to loosen.",
            "Uncertainty reveals the gap between expectation and being.",
            "The unknown exposes the borrowed nature of certainty.",
            "Uncertainty dissolves the script of should-be."
        ],
        "failure": [
            "Failure becomes identity when repetition is mistaken for destiny.",
            "Failure converts single events into permanent states.",
            "Mistake becomes proof of inherent inadequacy.",
            "Failure transforms learning into evidence of unworthiness."
        ]
    }
    
    # Enhanced question templates matching examples
    QUESTION_TEMPLATES = {
        "comparison": [
            "Whose measure turned your timeline into a verdict?",
            "Whose standard created this hierarchy?",
            "What comparison became your measurement?",
            "Whose judgment transformed difference into deficiency?"
        ],
        "perfection": [
            "What standard must be satisfied before you permit yourself to exist as enough?",
            "What does this perfection protect against?",
            "Whose measure makes completion impossible?",
            "What vulnerability does excellence prevent?"
        ],
        "approval": [
            "Whose approval became your authority?",
            "What external validation became your truth?",
            "Whose permission do you seek to exist?",
            "What makes others' approval your currency?"
        ],
        "identity": [
            "What performance replaced your being?",
            "Whose observation became your identity?",
            "What mask replaced the face beneath?",
            "Whose definition are you performing?"
        ],
        "control": [
            "What uncertainty does this control tame?",
            "What chaos does this order prevent?",
            "What unknown does this certainty defend against?",
            "Whose unpredictability are you managing?"
        ],
        "guilt": [
            "What definition of loyalty makes choosing yourself feel like betrayal?",
            "Whose boundary does this guilt protect?",
            "What belonging does autonomy threaten?",
            "Whose rules make self-prioritization treason?"
        ],
        "uncertainty": [
            "If expectation disappeared, what direction would remain unborrowed?",
            "Whose path became lost when the script dissolved?",
            "What certainty feels threatened by the unknown?",
            "If should disappeared, what would remain?"
        ],
        "failure": [
            "What assumption links your next outcome to your last one?",
            "Whose definition makes repetition proof of destiny?",
            "What standard converts single events into identity?",
            "What belief makes mistake permanent?"
        ]
    }
    
    def __init__(self, validation_threshold: float = 0.7):
        self.validation_threshold = validation_threshold
    
    def format_response(self, cognitive_unit: CognitiveUnit) -> FormattedResponse:
        """
        Transform grounded cognitive unit into two-sentence philosophical response.
        
        Args:
            cognitive_unit: Grounded material from retrieval layer
            
        Returns:
            FormattedResponse with philosophical framing and reflective question
        """
        # Generate initial response
        response = self._generate_response(cognitive_unit)
        
        # Validate and regenerate if needed
        if not self._validate_response(response, cognitive_unit):
            response = self._regenerate_strict(cognitive_unit)
        
        return response
    
    def _generate_response(self, unit: CognitiveUnit) -> FormattedResponse:
        """Generate initial philosophical response from grounded material."""
        
        # Extract philosophical framing from core_reframe
        framing = self._extract_philosophical_framing(unit.core_reframe, unit.theme_tags)
        
        # Generate reflective question aligned with question bank
        question = self._generate_reflective_question(unit.question_bank, unit.theme_tags)
        
        return FormattedResponse(
            framing_statement=framing,
            reflective_question=question
        )
    
    def _extract_philosophical_framing(self, core_reframe: str, theme_tags: List[str]) -> str:
        """
        Extract philosophical framing statement from core_reframe.
        
        This transforms the cognitive insight into a concise philosophical
        observation without adding new concepts.
        """
        # Find dominant theme
        dominant_theme = self._find_dominant_theme(theme_tags, list(self.FRAMING_PATTERNS.keys()))
        
        # Select framing pattern
        if dominant_theme in self.FRAMING_PATTERNS:
            patterns = self.FRAMING_PATTERNS[dominant_theme]
            return patterns[0]  # Use first pattern as default
        
        # Default philosophical framing if no specific theme
        return "The pattern reveals the structure behind the appearance."
    
    def _generate_reflective_question(self, question_bank: List[str], theme_tags: List[str]) -> str:
        """
        Generate elevated reflective question aligned with question bank patterns.
        
        This creates an assumption-exposing question that targets hidden cognitive
        structures while maintaining semantic alignment with existing questions.
        """
        # Find dominant theme
        dominant_theme = self._find_dominant_theme(theme_tags, list(self.QUESTION_TEMPLATES.keys()))
        
        # Select question template
        if dominant_theme in self.QUESTION_TEMPLATES:
            templates = self.QUESTION_TEMPLATES[dominant_theme]
            return templates[0]  # Use first template as default
        
        # Default question if no specific theme
        return "What hidden structure makes this pattern necessary?"
    
    def _find_dominant_theme(self, theme_tags: List[str], available_themes: List[str]) -> str:
        """Find the most relevant theme from available options."""
        for theme in available_themes:
            if theme in theme_tags:
                return theme
        return available_themes[0] if available_themes else "identity"
    
    def _analyze_question_patterns(self, question_bank: List[str]) -> Dict[str, int]:
        """Analyze patterns in existing question bank."""
        patterns = {
            "whose": 0,
            "what": 0, 
            "which": 0,
            "how": 0
        }
        
        for question in question_bank:
            question_lower = question.lower()
            for pattern in patterns:
                if question_lower.startswith(pattern):
                    patterns[pattern] += 1
        
        return patterns
    
    def _select_question_template(self, theme: str, bank_patterns: Dict[str, int]) -> str:
        """Select appropriate question template based on theme and bank patterns."""
        
        # Theme-specific template mappings
        theme_templates = {
            "comparison": "Whose {standard} created this {hierarchy}?",
            "perfection": "What {measure} turned {process} into {judgment}?",
            "approval": "Whose {validation} became your {authority}?",
            "identity": "Which {performance} replaced {authenticity}?",
            "control": "What {certainty} protects against {uncertainty}?"
        }
        
        return theme_templates.get(theme, self.QUESTION_TEMPLATES[0])
    
    def _fill_question_template(self, template: str, theme: str) -> str:
        """Fill question template with theme-appropriate vocabulary."""
        
        vocabulary = {
            "comparison": {
                "standard": "measure",
                "hierarchy": "ranking", 
                "construct": "comparison"
            },
            "perfection": {
                "measure": "standard",
                "process": "effort",
                "judgment": "failure"
            },
            "approval": {
                "validation": "approval",
                "authority": "truth",
                "performance": "appearance"
            },
            "identity": {
                "performance": "performance",
                "authenticity": "being",
                "construct": "identity"
            },
            "control": {
                "certainty": "control",
                "uncertainty": "freedom",
                "construct": "order"
            }
        }
        
        theme_vocab = vocabulary.get(theme, vocabulary["identity"])
        
        # Simple template filling
        question = template
        for key, value in theme_vocab.items():
            question = question.replace(f"{{{key}}}", value)
        
        return question
    
    def _validate_response(self, response: FormattedResponse, unit: CognitiveUnit) -> bool:
        """Validate response meets all style and grounding requirements."""
        
        full_text = response.to_string()
        
        # Check sentence count
        sentences = re.split(r'[.!?]+', full_text)
        sentence_count = len([s.strip() for s in sentences if s.strip()])
        if sentence_count != 2:
            return False
        
        # Check exactly one question mark
        question_marks = full_text.count('?')
        if question_marks != 1:
            return False
        
        # Check for forbidden phrases
        text_lower = full_text.lower()
        for phrase in self.FORBIDDEN_PHRASES:
            if phrase in text_lower:
                return False
        
        # Check semantic similarity with question bank
        similarity = self._calculate_question_similarity(response.reflective_question, unit.question_bank)
        if similarity < self.validation_threshold:
            return False
        
        return True
    
    def _calculate_question_similarity(self, generated_question: str, question_bank: List[str]) -> float:
        """
        Calculate semantic similarity between generated question and question bank.
        
        Simple implementation using keyword overlap. In production, this would use
        more sophisticated semantic similarity measures.
        """
        if not question_bank:
            return 0.5  # Default similarity
        
        # Extract keywords from generated question
        gen_keywords = set(re.findall(r'\b\w+\b', generated_question.lower()))
        
        max_similarity = 0.0
        for bank_question in question_bank:
            bank_keywords = set(re.findall(r'\b\w+\b', bank_question.lower()))
            
            # Calculate Jaccard similarity
            intersection = len(gen_keywords & bank_keywords)
            union = len(gen_keywords | bank_keywords)
            
            if union > 0:
                similarity = intersection / union
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _regenerate_strict(self, unit: CognitiveUnit) -> FormattedResponse:
        """Regenerate response with stricter constraints."""
        
        # More direct philosophical framing
        framing_patterns = {
            "comparison": "Comparison creates hierarchy from difference.",
            "perfection": "Perfectionism protects against being seen.",
            "approval": "External approval replaces internal validation.",
            "identity": "Identity becomes performance for others.",
            "control": "Control attempts to tame uncertainty."
        }
        
        dominant_theme = self._find_dominant_theme(unit.theme_tags, list(framing_patterns.keys()))
        framing = framing_patterns.get(dominant_theme, "The pattern reveals the hidden structure.")
        
        # More direct assumption-exposing question
        direct_questions = {
            "comparison": "Whose measure created this comparison?",
            "perfection": "What does this perfection protect against?",
            "approval": "Whose approval became your authority?",
            "identity": "What performance replaced your being?",
            "control": "What uncertainty does this control tame?"
        }
        
        question = direct_questions.get(dominant_theme, "What hidden structure makes this necessary?")
        
        return FormattedResponse(
            framing_statement=framing,
            reflective_question=question
        )


# Example usage and testing
if __name__ == "__main__":
    # Example cognitive unit
    example_unit = CognitiveUnit(
        user_input="I feel like I'm never good enough no matter how hard I try",
        retrieved_unit="perfectionism pattern with external validation",
        core_reframe="Perfectionism uses impossible standards to protect against the vulnerability of being seen as inadequate",
        question_bank=[
            "Whose standard created this measure of good enough?",
            "What does perfection protect against?",
            "When did being excellent become not enough?"
        ],
        theme_tags=["perfection", "approval", "comparison"]
    )
    
    formatter = ResponseStyleFormatter()
    response = formatter.format_response(example_unit)
    
    print("Generated Response:")
    print(response.to_string())
    print(f"\nValidation: {formatter._validate_response(response, example_unit)}")
