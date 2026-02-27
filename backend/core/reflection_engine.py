from vector_store import get_vectordb
from core.llm.llm_client import call_llm
from core.constraint_validator.validator import validate_response
from core.prompt_manager.prompt_builder import build_prompt

def run_reflection(user_input: str):
    """
    Run reflection with clean architecture:
    1. Retrieve cognitive pattern from persistent Chroma
    2. Build structured prompt with retrieval context
    3. Generate natural reflective response via LLM
    4. Validate response constraints
    5. Return stable result
    """
    
    # 1. Retrieve cognitive pattern from persistent vector store
    vectordb = get_vectordb()
    docs = vectordb.similarity_search(user_input, k=1)
    
    retrieved_chunk = docs[0].page_content if docs else ""
    
    # 2. Build structured prompt with retrieval context
    prompt = build_prompt(user_input, retrieved_chunk)
    
    # 3. Generate natural reflective response
    raw_response = call_llm(prompt)
    
    # 4. Validate response constraints
    final_response = validate_response(raw_response)
    
    # 5. Return validated result
    return final_response
