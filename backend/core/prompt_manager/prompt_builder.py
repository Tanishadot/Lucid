from core.prompt_manager.system_prompt import SYSTEM_PROMPT

def build_prompt(user_input: str):
    return f"""
{SYSTEM_PROMPT}

User input:
{user_input}

Generate a minimal reflective response with at most one question.
"""