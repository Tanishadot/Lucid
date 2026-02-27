from core.prompt_manager.system_prompt import SYSTEM_PROMPT

def build_prompt(user_input: str, retrieved_chunk: str = ""):
    """
    Build structured reflection prompt with retrieval context.
    
    Args:
        user_input: The user's input message
        retrieved_chunk: Retrieved cognitive pattern from vector store
        
    Returns:
        Formatted prompt for LLM generation
    """
    
    # Add retrieval context only if available
    cognitive_context = ""
    if retrieved_chunk:
        cognitive_context = f"""
Cognitive context:
{retrieved_chunk}
"""
    
    return f"""
{SYSTEM_PROMPT}

{cognitive_context}

User input:
{user_input}

Generate a minimal reflective response.
Ask only ONE natural question.
Do not quote the cognitive context.
Do not give advice.
"""