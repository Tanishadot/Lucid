import re

def validate_response(response: str) -> str:
    """
    Validate single reflective question constraints:
    - Enforce exactly one question mark
    - Ensure response ends with question mark
    - Remove periods before question mark
    - Avoid multiple interrogative clauses
    - Strip introductory statements
    - Ensure intellectual precision
    """
    
    # Clean whitespace
    response = response.strip()
    
    # Count questions
    question_count = response.count('?')
    
    # If multiple questions, keep only the strongest (longest meaningful interrogative clause)
    if question_count > 1:
        # Split by question marks and find the most substantial question
        questions = [q.strip() for q in response.split('?') if q.strip()]
        # Find the longest question (likely most substantial)
        strongest_question = max(questions, key=len) if questions else ""
        response = strongest_question + '?'
    
    # Remove any periods before question mark
    response = re.sub(r'\.+\?', '?', response)
    
    # Strip any introductory statements before the question
    # Look for patterns like "Statement. Question" or "Statement? Question?"
    if '?' in response:
        question_start = response.rfind('?')
        if question_start > 0:
            # Check if there's content before the last question
            before_question = response[:question_start + 1]
            after_question = response[question_start + 1:].strip()
            
            # If there's substantial content before, extract just the question part
            if after_question and len(after_question) > 10:
                # Find the actual question in the after part
                question_match = re.search(r'[^.!?]*\?', after_question)
                if question_match:
                    response = question_match.group(0).strip()
            else:
                # Look for question in the whole response
                question_match = re.search(r'[^.!?]*\?', response)
                if question_match:
                    response = question_match.group(0).strip()
    
    # Ensure response ends with exactly one question mark
    if not response.endswith('?'):
        response = response.rstrip('!?') + '?'
    
    # Remove multiple consecutive question marks
    response = re.sub(r'\?+', '?', response)
    
    # STRICT FORBIDDEN PATTERNS - Reject entire response if found
    forbidden_openings = [
        "it sounds like", "it seems", "you seem to", 
        "you are experiencing", "the situation", "it appears that",
        "it looks like", "you are connecting", "it appears"
    ]
    
    forbidden_questions = [
        "what feelings arise", "how did that make you feel", 
        "why do you think", "what caused", "what led to", 
        "what made you", "what contributed to", "what specific qualities",
        "what experiences led you", "what criteria are you using",
        "how does that make you feel", "what do you think about that"
    ]
    
    lower_response = response.lower()
    
    # Check for forbidden openings
    for opening in forbidden_openings:
        if opening in lower_response:
            return "What belief beneath this feels unquestionable to you?"
    
    # Check for forbidden questions
    for question in forbidden_questions:
        if question in lower_response:
            return "What belief beneath this feels unquestionable to you?"
    
    # Check for multiple interrogative clauses joined by conjunctions
    interrogative_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which']
    clause_count = sum(1 for word in interrogative_words if word in lower_response.split())
    
    if clause_count > 1:
        # Keep only the first substantial interrogative clause
        words = response.split()
        clause_end = -1
        for i, word in enumerate(words):
            if word.lower() in interrogative_words and i > 0:
                clause_end = i
                break
        
        if clause_end > 0:
            response = ' '.join(words[:clause_end + 5]) + '?'  # Keep a few more words for context
            response = re.sub(r'\?+', '?', response)
    
    # Remove extra whitespace and ensure single line
    response = re.sub(r'\s+', ' ', response).strip()
    
    # Final validation: ensure it's a single, meaningful question
    if len(response) < 10 or '?' not in response:
        return "What belief beneath this feels unquestionable to you?"
    
    return response
