"""
Integration Layer for ResponseStyleFormatter

Shows how to integrate the style formatter into existing API endpoints
without changing retrieval logic or architecture.
"""

from typing import Dict, Any
from services.response_style_formatter import ResponseStyleFormatter, CognitiveUnit, FormattedResponse


class LucidResponsePipeline:
    """
    Integration layer that adds style formatting to existing cognitive responses.
    
    This wraps existing retrieval/response logic with the style formatter
    without modifying the underlying cognitive architecture.
    """
    
    def __init__(self):
        self.style_formatter = ResponseStyleFormatter()
    
    def format_cognitive_response(
        self,
        user_input: str,
        retrieved_unit: str,
        core_reframe: str,
        question_bank: list,
        theme_tags: list
    ) -> Dict[str, Any]:
        """
        Apply style formatting to grounded cognitive material.
        
        This method takes the output from existing retrieval/logic layers
        and applies the philosophical style constraints.
        
        Args:
            user_input: Original user input
            retrieved_unit: Material from retrieval layer
            core_reframe: Core cognitive reframing insight
            question_bank: Existing question patterns
            theme_tags: Identified cognitive themes
            
        Returns:
            Formatted response with metadata
        """
        
        # Create cognitive unit from existing materials
        cognitive_unit = CognitiveUnit(
            user_input=user_input,
            retrieved_unit=retrieved_unit,
            core_reframe=core_reframe,
            question_bank=question_bank,
            theme_tags=theme_tags
        )
        
        # Apply style formatting
        formatted_response = self.style_formatter.format_response(cognitive_unit)
        
        # Return structured response
        return {
            "response": formatted_response.to_string(),
            "framing_statement": formatted_response.framing_statement,
            "reflective_question": formatted_response.reflective_question,
            "theme_tags": theme_tags,
            "style_applied": True,
            "validation_passed": True
        }


# Example integration with existing API endpoint
def integrate_with_existing_api():
    """
    Example showing how to integrate with existing /api/v1/reflect endpoint.
    
    This would be added to the existing endpoint logic without changing
    the retrieval or cognitive processing.
    """
    
    pipeline = LucidResponsePipeline()
    
    # This would be inserted into existing API logic after retrieval
    def apply_style_formatting(existing_response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply style formatting to existing API response.
        
        This function would be called after the existing cognitive processing
        but before returning the response to the client.
        """
        
        # Extract existing cognitive material
        user_input = existing_response_data.get("user_input", "")
        retrieved_insight = existing_response_data.get("cognitive_insight", "")
        core_reframe = existing_response_data.get("core_reframe", "")
        question_patterns = existing_response_data.get("question_patterns", [])
        identified_themes = existing_response_data.get("theme_tags", [])
        
        # Apply style formatting
        styled_response = pipeline.format_cognitive_response(
            user_input=user_input,
            retrieved_unit=retrieved_insight,
            core_reframe=core_reframe,
            question_bank=question_patterns,
            theme_tags=identified_themes
        )
        
        # Merge with existing response data
        return {
            **existing_response_data,
            **styled_response
        }
    
    return apply_style_formatting


# Testing the integration
if __name__ == "__main__":
    # Example existing response data (from current API)
    existing_response = {
        "user_input": "I feel like I'm never good enough no matter how hard I try",
        "cognitive_insight": "perfectionism pattern with external validation",
        "core_reframe": "Perfectionism uses impossible standards to protect against the vulnerability of being seen as inadequate",
        "question_patterns": [
            "Whose standard created this measure of good enough?",
            "What does perfection protect against?"
        ],
        "theme_tags": ["perfection", "approval", "comparison"],
        "depth": "pattern"
    }
    
    # Apply style formatting
    integration_func = integrate_with_existing_api()
    styled_response = integration_func(existing_response)
    
    print("Original Response:")
    print(existing_response.get("response", "No original response"))
    
    print("\nStyled Response:")
    print(styled_response["response"])
    
    print(f"\nFraming: {styled_response['framing_statement']}")
    print(f"Question: {styled_response['reflective_question']}")
    print(f"Themes: {styled_response['theme_tags']}")
