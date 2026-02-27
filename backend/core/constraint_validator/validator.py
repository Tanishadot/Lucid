import re

def validate_response(response: str) -> str:
    """
    Validate LUCID response constraints:
    - Remove directive language
    - Ensure only one question
    - Clean whitespace
    - No advice
    - No reassurance
    - No philosophical quoting
    """
    
    # Clean whitespace
    response = response.strip()
    
    # Count questions
    question_count = response.count('?')
    
    # If multiple questions, keep only the first
    if question_count > 1:
        first_question = response.find('?')
        response = response[:first_question + 1]
    
    # Remove directive phrases
    forbidden_phrases = [
        "you should", "try to", "it may help", "you must", "you need to",
        "I suggest", "I recommend", "consider", "think about", "it would be"
    ]
    
    lower_response = response.lower()
    for phrase in forbidden_phrases:
        if phrase in lower_response:
            response = response.replace(phrase, "")
    
    # Remove reassurance phrases
    reassurance_phrases = [
        "it's okay", "that's normal", "don't worry",
        "it's alright", "you're not alone", "that's fine"
    ]
    
    for phrase in reassurance_phrases:
        if phrase in lower_response:
            response = response.replace(phrase, "")
    
    # Remove extra whitespace
    response = re.sub(r'\s+', ' ', response).strip()
    
    return response