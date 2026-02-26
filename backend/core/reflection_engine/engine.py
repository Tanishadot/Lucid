from core.prompt_manager.prompt_builder import build_prompt
from services.llm_service import call_llm
from core.constraint_validator.validator import validate_response

def run_reflection(user_input: str):
    prompt = build_prompt(user_input)
    raw_response = call_llm(prompt)
    final_response = validate_response(raw_response)
    return final_response