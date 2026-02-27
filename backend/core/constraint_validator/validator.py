import re

def validate_response(response: str):
    # Remove directive language
    forbidden_phrases = ["you should", "try to", "it may help", "you must", "you need to"]
    lower = response.lower()
    for phrase in forbidden_phrases:
        if phrase in lower:
            response = response.replace(phrase, "")
    
    # Ensure only one question
    if response.count("?") > 1:
        first = response.find("?")
        response = response[:first+1]
    
    # Remove extra whitespace
    response = re.sub(r'\s+', ' ', response).strip()
    
    return response