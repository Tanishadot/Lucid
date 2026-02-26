import re

def validate_response(response: str):
    forbidden_phrases = ["you should", "try to", "it may help"]
    lower = response.lower()
    for phrase in forbidden_phrases:
        if phrase in lower:
            response = response.replace(phrase, "")
    # Ensure only one question
    if response.count("?") > 1:
        first = response.find("?")
        response = response[:first+1]
    return response.strip()