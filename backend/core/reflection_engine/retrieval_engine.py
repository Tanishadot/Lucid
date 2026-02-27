from core.prompt_manager.prompt_builder import build_prompt
from services.llm_service import call_llm
from core.constraint_validator.validator import validate_response
from knowledge.vector_store.retriever import retrieve_reflection_unit

def run_reflection(user_input: str):
    """
    Run a retrieval-grounded reflection process.
    
    Args:
        user_input: The user's input message
        
    Returns:
        str: A reflective response based on retrieved knowledge
    """
    # Step 1: Retrieve relevant reflection unit
    reflection_unit = retrieve_reflection_unit(user_input)
    
    # Step 2: Build prompt with retrieved content
    prompt = build_retrieval_aware_prompt(
        user_input=user_input,
        reframe=reflection_unit["reframe"],
        question=reflection_unit["question"]
    )
    
    # Step 3: Get LLM response (low temperature for consistency)
    raw_response = call_llm(prompt, temperature=0.2)
    
    # Step 4: Validate and return response
    final_response = validate_response(raw_response)
    return final_response

def build_retrieval_aware_prompt(user_input: str, reframe: str, question: str) -> str:
    """
    Build a prompt that incorporates retrieved knowledge.
    
    Args:
        user_input: The user's input message
        reframe: The retrieved reframe text
        question: The retrieved question
        
    Returns:
        str: A formatted prompt for the LLM
    """
    from core.prompt_manager.system_prompt import SYSTEM_PROMPT
    
    prompt = f"""
{SYSTEM_PROMPT}

Retrieved Reflection:
Reframe: {reframe}
Question: {question}

User input:
{user_input}

Instructions:
- Respond minimally.
- Use the provided reframe.
- Ask ONLY the provided question.
- Do not generate a new question.
- Keep the response concise and direct.
"""
    
    return prompt
