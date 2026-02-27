import json
import os

# Simple pattern-based retrieval as fallback
def simple_pattern_retrieval(user_input: str) -> dict:
    """
    Simple pattern-based retrieval when Chroma is having issues
    """
    user_lower = user_input.lower()
    
    # Pattern mappings based on common cognitive patterns
    patterns = {
        "failing": {
            "reframe": "The feeling of failing often comes from measuring against impossible standards that were never meant to be human.",
            "question": "What would it look like to separate your worth from your performance?"
        },
        "perfectionism": {
            "reframe": "Perfectionism is often the armor that protects us from the shame of not being enough.",
            "question": "What would happen if you allowed yourself to be imperfect and still worthy?"
        },
        "tired": {
            "reframe": "Exhaustion often signals that we're carrying more than we were meant to carry alone.",
            "question": "What part of this exhaustion comes from trying to be everything for everyone?"
        },
        "anxious": {
            "reframe": "Anxiety is often the body's way of telling us there's something important that needs attention.",
            "question": "What is this anxiety trying to protect you from feeling?"
        },
        "stuck": {
            "reframe": "Being stuck often means we're standing at the edge of growth, not failure.",
            "question": "What does being stuck protect you from having to face?"
        }
    }
    
    # Check for pattern matches
    for pattern_key, pattern_data in patterns.items():
        if pattern_key in user_lower:
            print(f"=== PATTERN MATCH: {pattern_key} ===")
            return pattern_data
    
    # Default fallback
    return {
        "reframe": "",
        "question": "What feels most present for you in this moment?"
    }

# Test the function
if __name__ == "__main__":
    test_inputs = [
        "I feel like I am failing at everything lately",
        "I'm so tired after being with people",
        "I feel anxious about everything",
        "I feel stuck in my life"
    ]
    
    for test_input in test_inputs:
        print(f"\nInput: {test_input}")
        result = simple_pattern_retrieval(test_input)
        print(f"Result: {result}")
        print("-" * 50)
