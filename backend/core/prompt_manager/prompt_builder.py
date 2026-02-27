from core.prompt_manager.system_prompt import SYSTEM_PROMPT

def build_prompt(user_input: str, retrieved_chunk: str = ""):
    """
    Build single reflective question prompt with retrieval context.
    
    Args:
        user_input: The user's input message
        retrieved_chunk: Retrieved cognitive pattern from vector store
        
    Returns:
        Formatted prompt for single question generation
    """
    
    # Add retrieval context only if available
    cognitive_context = ""
    if retrieved_chunk:
        cognitive_context = f"""
Cognitive context:
{retrieved_chunk}
"""
    
    instruction = """
Task:
Generate EXACTLY ONE philosophically precise reflective question.
The question must:
- Contain one sentence only.
- End with a single '?'.
- Avoid generic phrasing.
- Challenge a hidden assumption or internal standard.
- Not include explanations or statements before the question.

If output does not meet these constraints, regenerate internally before returning.
"""
    
    return f"""
{SYSTEM_PROMPT}

{cognitive_context}

User input:
{user_input}

{instruction}
"""