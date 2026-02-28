from core.prompt_manager.system_prompt import SYSTEM_PROMPT

def build_prompt(user_input: str, retrieved_unit: dict = None):
    """
    Build two-sentence philosophical prompt with retrieval context.
    
    Args:
        user_input: The user's input message
        retrieved_unit: Retrieved cognitive unit containing:
            - cognitive_pattern
            - core_reframe
            - question_bank
            - rewire_target
            - theme_tags
        
    Returns:
        Formatted prompt for two-sentence philosophical response generation
    """
    
    # Add retrieval context only if available
    cognitive_context = ""
    if retrieved_unit:
        cognitive_context = f"""
Retrieved Cognitive Unit:
Cognitive Pattern: {retrieved_unit.get('cognitive_pattern', 'Unknown')}
Core Reframe: {retrieved_unit.get('core_reframe', '')}
Question Bank: {retrieved_unit.get('question_bank', [])}
Rewire Target: {retrieved_unit.get('rewire_target', '')}
Theme Tags: {retrieved_unit.get('theme_tags', [])}
"""
    
    instruction = """
Task:
Generate EXACTLY TWO sentences:

1. Sentence One: A concise philosophical reframing statement derived from the retrieved core_reframe.
   - Must align with theme_tags and cognitive_pattern.
   - Must not introduce new conceptual domains.
   - Must be precise and minimal.

2. Sentence Two: EXACTLY ONE elevated reflective question.
   - Must end with exactly one '?'.
   - Must align with question_bank patterns.
   - Must challenge a hidden assumption, identity, belief, or internal standard.
   - Must not directly ask about feelings.
   - Must avoid generic phrasing.

No additional sentences.
No additional questions.
No extra commentary.

If structure is violated, regenerate internally once with stricter precision.
"""
    
    return f"""
{SYSTEM_PROMPT}

{cognitive_context}

User input:
{user_input}

{instruction}
"""