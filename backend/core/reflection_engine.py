from vector_store import get_vectordb
from core.llm.llm_client import call_llm
from core.constraint_validator.validator import validate_response
from core.prompt_manager.prompt_builder import build_prompt

def score_question_quality(question: str) -> int:
    """
    Score question for quality metrics:
    - Specificity (no generic phrasing)
    - Assumption exposure
    - Identity depth
    - Intellectual tension
    """
    score = 0
    lower_question = question.lower()
    
    # Specificity: penalize generic therapy phrases
    generic_phrases = [
        "how does that make you feel",
        "what do you think about that",
        "why do you think that",
        "what criteria are you using",
        "how did that make you feel"
    ]
    for phrase in generic_phrases:
        if phrase in lower_question:
            score -= 2
    
    # Assumption exposure: reward challenging assumptions
    assumption_words = [
        "assumption", "standard", "belief", "identity", "definition",
        "comparison", "hierarchy", "responsible", "intention"
    ]
    for word in assumption_words:
        if word in lower_question:
            score += 1
    
    # Identity depth: reward deep identity questions
    identity_words = [
        "become", "define", "identity", "self", "who", "what are you"
    ]
    for word in identity_words:
        if word in lower_question:
            score += 1
    
    # Intellectual tension: reward thought-provoking structure
    tension_patterns = [
        "what makes", "what creates", "what transforms", "what converts",
        "what distinguishes", "what separates", "what enables"
    ]
    for pattern in tension_patterns:
        if pattern in lower_question:
            score += 1
    
    # Penalize multiple questions
    if question.count('?') > 1:
        score -= 3
    
    # Penalize statements before question
    if '?' in question:
        question_pos = question.find('?')
        if question_pos > 10:  # Substantial content before question
            score -= 2
    
    return score

def is_generic_therapy_response(question: str) -> bool:
    """
    Check if response sounds like standard therapy phrasing
    """
    lower_question = question.lower()
    generic_patterns = [
        "how does that make you feel",
        "what do you think about that",
        "why do you think that",
        "what criteria are you using",
        "how did that make you feel",
        "tell me more about",
        "describe that feeling"
    ]
    return any(pattern in lower_question for pattern in generic_patterns)

def run_reflection(user_input: str):
    """
    Run reflection with clean architecture:
    1. Retrieve cognitive pattern from persistent Chroma
    2. Build structured prompt with retrieval context
    3. Generate natural reflective response via LLM
    4. Apply internal quality filter
    5. Validate response constraints
    6. Return stable result
    """
    
    # 1. Retrieve cognitive pattern from persistent vector store
    vectordb = get_vectordb()
    docs = vectordb.similarity_search(user_input, k=1)
    
    retrieved_chunk = docs[0].page_content if docs else ""
    
    # 2. Build structured prompt with retrieval context
    prompt = build_prompt(user_input, retrieved_chunk)
    
    # 3. Generate natural reflective response
    raw_response = call_llm(prompt)
    
    # 4. Apply internal quality filter
    quality_score = score_question_quality(raw_response)
    
    # If quality is low, regenerate with stricter instruction
    if quality_score < 2 or is_generic_therapy_response(raw_response):
        stricter_prompt = prompt + "\n\nMake the question sharper and more assumption-exposing."
        raw_response = call_llm(stricter_prompt)
    
    # 5. Validate response constraints
    final_response = validate_response(raw_response)
    
    # 6. Return validated result
    return final_response
