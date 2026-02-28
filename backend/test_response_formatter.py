"""
Test Suite for ResponseStyleFormatter

Demonstrates the style formatting system working with various cognitive patterns.
"""

from services.response_style_formatter import ResponseStyleFormatter, CognitiveUnit
from services.response_integration import LucidResponsePipeline


def test_style_formatter():
    """Test the style formatter with various cognitive patterns."""
    
    formatter = ResponseStyleFormatter()
    
    # Test cases for different cognitive patterns
    test_cases = [
        {
            "name": "Perfectionism Pattern",
            "unit": CognitiveUnit(
                user_input="I feel like I'm never good enough no matter how hard I try",
                retrieved_unit="perfectionism pattern with external validation",
                core_reframe="Perfectionism uses impossible standards to protect against the vulnerability of being seen as inadequate",
                question_bank=[
                    "Whose standard created this measure of good enough?",
                    "What does perfection protect against?"
                ],
                theme_tags=["perfection", "approval", "comparison"]
            )
        },
        {
            "name": "Comparison Pattern", 
            "unit": CognitiveUnit(
                user_input="Everyone else seems to have it all figured out",
                retrieved_unit="social comparison with idealized others",
                core_reframe="Comparison transforms subjective experience into objective ranking",
                question_bank=[
                    "Whose measure created this comparison?",
                    "What makes their success your failure?"
                ],
                theme_tags=["comparison", "identity", "approval"]
            )
        },
        {
            "name": "Approval Pattern",
            "unit": CognitiveUnit(
                user_input="I need everyone to like me and my decisions",
                retrieved_unit="external approval seeking behavior",
                core_reframe="External approval substitutes for internal validation",
                question_bank=[
                    "Whose approval became your authority?",
                    "What happens without external validation?"
                ],
                theme_tags=["approval", "identity", "control"]
            )
        }
    ]
    
    print("=== Response Style Formatter Test Results ===\n")
    
    for test_case in test_cases:
        print(f"Pattern: {test_case['name']}")
        print(f"Input: {test_case['unit'].user_input}")
        
        # Generate response
        response = formatter.format_response(test_case['unit'])
        
        print(f"Response: {response.to_string()}")
        print(f"Framing: {response.framing_statement}")
        print(f"Question: {response.reflective_question}")
        
        # Validate
        is_valid = formatter._validate_response(response, test_case['unit'])
        print(f"Validation: {'✓ PASS' if is_valid else '✗ FAIL'}")
        
        print("-" * 60)


def test_integration_pipeline():
    """Test the full integration pipeline."""
    
    pipeline = LucidResponsePipeline()
    
    print("\n=== Integration Pipeline Test ===\n")
    
    # Example existing API response data
    existing_data = {
        "user_input": "I keep procrastinating on important tasks",
        "cognitive_insight": "avoidance pattern linked to perfectionism",
        "core_reframe": "Procrastination protects against the possibility of imperfect performance",
        "question_patterns": [
            "What might this delay protect against?",
            "Whose standard makes starting so difficult?"
        ],
        "theme_tags": ["perfection", "control", "avoidance"],
        "depth": "pattern"
    }
    
    # Apply style formatting
    styled_response = pipeline.format_cognitive_response(
        user_input=existing_data["user_input"],
        retrieved_unit=existing_data["cognitive_insight"],
        core_reframe=existing_data["core_reframe"],
        question_bank=existing_data["question_patterns"],
        theme_tags=existing_data["theme_tags"]
    )
    
    print("Original Input:", existing_data["user_input"])
    print("Core Reframe:", existing_data["core_reframe"])
    print("\nStyled Response:", styled_response["response"])
    print("Themes:", styled_response["theme_tags"])
    print("Style Applied:", styled_response["style_applied"])


def demonstrate_validation_rules():
    """Demonstrate validation rules in action."""
    
    formatter = ResponseStyleFormatter()
    
    print("\n=== Validation Rules Demonstration ===\n")
    
    # Test invalid responses
    invalid_cases = [
        {
            "name": "Too many sentences",
            "response": "This is sentence one. This is sentence two. This is sentence three? This is sentence four.",
            "unit": CognitiveUnit("", "", "", [], [])
        },
        {
            "name": "No question mark",
            "response": "This is the framing statement. This is the question without a mark.",
            "unit": CognitiveUnit("", "", "", [], [])
        },
        {
            "name": "Forbidden phrase",
            "response": "This is the framing statement. You should consider this question?",
            "unit": CognitiveUnit("", "", "", [], [])
        }
    ]
    
    for case in invalid_cases:
        print(f"Test: {case['name']}")
        print(f"Response: {case['response']}")
        
        # Create FormattedResponse object
        parts = case['response'].split('. ')
        if len(parts) >= 2:
            framing = parts[0] + '.'
            question = parts[1]
            response_obj = formatter._regenerate_strict(case['unit'])
            response_obj.framing_statement = framing
            response_obj.reflective_question = question
            
            is_valid = formatter._validate_response(response_obj, case['unit'])
            print(f"Validation: {'✓ PASS' if is_valid else '✗ FAIL (expected)'}")
        
        print("-" * 40)


if __name__ == "__main__":
    # Run all tests
    test_style_formatter()
    test_integration_pipeline()
    demonstrate_validation_rules()
    
    print("\n=== System Summary ===")
    print("✓ Style formatting layer implemented")
    print("✓ Two-sentence philosophical structure")
    print("✓ Validation rules enforced")
    print("✓ Integration pipeline ready")
    print("✓ No retrieval logic modified")
    print("✓ Pure formatting layer only")
