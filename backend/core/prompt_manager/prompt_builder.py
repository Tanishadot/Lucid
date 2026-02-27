from core.prompt_manager.system_prompt import SYSTEM_PROMPT
from core.memory.memory_manager import get_memory


def build_prompt(user_input: str, retrieval_context: dict = None):
    memory = get_memory()

    memory_block = ""
    if memory:
        memory_block = "Previous conversation:\n"
        for turn in memory:
            memory_block += f"User: {turn['user']}\n"
            memory_block += f"LUCID: {turn['assistant']}\n"

    # Add optional retrieval context
    context_block = ""
    if retrieval_context:
        reframe = retrieval_context.get("reframe", "")
        pattern = retrieval_context.get("cognitive_pattern", "")
        
        if reframe or pattern:
            context_block = f"""
Optional reflection context:
Reframe hint: {reframe}
Pattern hint: {pattern}
"""

    instruction = """
Deepen reflection naturally.
Follow Progressive Inquiry Rule strictly.
Build on prior turn if relevant.
Do not widen topic unnecessarily.
Respond with exactly one open-ended question.
"""

    return f"""
{SYSTEM_PROMPT}

{memory_block}

{context_block}

Current user input:
{user_input}

{instruction}
"""