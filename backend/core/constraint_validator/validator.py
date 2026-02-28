import re

def validate_response(response: str) -> str:
    """
    Validate two-sentence philosophical response constraints:
    - Enforce exactly two sentences
    - Enforce exactly one question mark
    - Ensure final character is '?'
    - Remove forbidden phrases
    - Maintain philosophical framing + question structure
    """
    
    # Clean whitespace
    response = response.strip()
    
    # Count question marks
    question_count = response.count('?')
    
    # FORBIDDEN PHRASES
    forbidden_phrases = [
        "you should",
        "it may help", 
        "consider",
        "try to",
        "remember that",
        "how does that make you feel",
        "what do you think",
        "why do you think",
        "what criteria are you using"
    ]
    
    # Check for forbidden phrases
    lower_response = response.lower()
    for phrase in forbidden_phrases:
        if phrase in lower_response:
            # Regenerate with fallback structure
            return "The pattern reveals the structure behind the appearance. What belief beneath this feels unquestioned?"
    
    # VALIDATION RULE 1: Exactly one question mark
    if question_count != 1:
        if question_count == 0:
            # No question - add fallback question
            sentences = re.split(r'[.!?]+', response)
            statements = [s.strip() for s in sentences if s.strip()]
            if statements:
                return f"{statements[0]}. What belief beneath this feels unquestioned?"
            else:
                return "The pattern reveals the structure behind the appearance. What belief beneath this feels unquestioned?"
        elif question_count > 1:
            # Multiple questions - keep only first question
            first_question_pos = response.find('?')
            response = response[:first_question_pos + 1]
    
    # VALIDATION RULE 2: Exactly two sentences
    sentences = re.split(r'[.!?]+', response)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) > 2:
        # Keep only first statement + first question
        statement = sentences[0]
        # Find the question sentence
        question_sentence = None
        for s in sentences[1:]:
            if '?' in s or any(word in s.lower() for word in ['what', 'why', 'how', 'which', 'who', 'when', 'where']):
                question_sentence = s
                break
        
        if question_sentence:
            response = f"{statement}. {question_sentence}"
        else:
            response = f"{statement}. What belief beneath this feels unquestioned?"
    
    elif len(sentences) == 1:
        # Only one sentence - check if it's a question or statement
        if '?' in sentences[0]:
            # It's a question - add framing statement
            response = f"The pattern reveals the structure behind the appearance. {sentences[0]}"
        else:
            # It's a statement - add question
            response = f"{sentences[0]}. What belief beneath this feels unquestioned?"
    
    # VALIDATION RULE 3: Final character must be '?'
    if not response.endswith('?'):
        response = response.rstrip('!?') + '?'
    
    # VALIDATION RULE 4: No additional interrogative clauses
    # Ensure only the final sentence is interrogative
    parts = response.split('. ')
    if len(parts) > 2:
        # Keep only first statement and final question
        response = f"{parts[0]}. {parts[-1]}"
    
    # VALIDATION RULE 5: Remove multiple consecutive punctuation
    response = re.sub(r'[!?]{2,}', '?', response)
    response = re.sub(r'\.\?', '.', response)
    
    # Normalize whitespace
    response = re.sub(r'\s+', ' ', response).strip()
    
    # Final validation: ensure exactly 2 sentences and 1 question
    final_sentences = re.split(r'[.!?]+', response)
    final_sentences = [s.strip() for s in final_sentences if s.strip()]
    final_questions = response.count('?')
    
    if len(final_sentences) != 2 or final_questions != 1:
        return "The pattern reveals the structure behind the appearance. What belief beneath this feels unquestioned?"
    
    return response


def lightweight_semantic_check(response: str, core_reframe: str = "", question_bank: list = None) -> bool:
    """
    Lightweight semantic alignment check.
    
    Args:
        response: Generated response
        core_reframe: Retrieved core reframing
        question_bank: Retrieved question patterns
        
    Returns:
        True if semantically aligned, False otherwise
    """
    if not core_reframe and not question_bank:
        return True  # No grounding to check against
    
    # Check if response shares keywords with core_reframe
    if core_reframe:
        core_keywords = set(core_reframe.lower().split())
        response_keywords = set(response.lower().split())
        keyword_overlap = len(core_keywords & response_keywords)
        
        # Require at least some keyword overlap
        if keyword_overlap < 2:
            return False
    
    # Check if question aligns with question_bank patterns
    if question_bank:
        question_part = response.split('?')[0] + '?' if '?' in response else response
        question_lower = question_part.lower()
        
        # Look for semantic similarity with question bank
        for bank_question in question_bank:
            bank_lower = bank_question.lower()
            bank_keywords = set(bank_lower.split())
            response_keywords = set(question_lower.split())
            
            # Simple keyword overlap check
            overlap = len(bank_keywords & response_keywords)
            if overlap >= 2:  # At least 2 overlapping keywords
                return True
        
        return False  # No semantic alignment found
    
    return True
