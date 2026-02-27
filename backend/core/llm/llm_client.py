from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def call_llm(prompt: str, temperature: float = 0.2) -> str:
    """
    Call LLM with natural reasoning while maintaining constraints.
    
    Args:
        prompt: The complete prompt including SYSTEM_PROMPT
        temperature: Low temperature for consistent responses
        
    Returns:
        str: Generated response
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are LUCID - a structured, non-directive reflection system."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"LLM call failed: {e}")
        return "What feels most present for you in this moment?"

def validate_response(response: str) -> str:
    """
    Validate response meets LUCID constraints.
    
    Args:
        response: Generated response
        
    Returns:
        str: Validated response
    """
    # Ensure exactly one question mark
    question_count = response.count('?')
    if question_count != 1:
        # Try to fix by removing extra question marks
        parts = response.split('?')
        if len(parts) > 1:
            response = parts[0] + '?' + ''.join(parts[1:])
        else:
            # Add question mark if missing
            response = response.rstrip('.') + '?'
    
    # Remove directive phrases
    directive_phrases = [
        "You should", "You must", "You need to",
        "I suggest", "I recommend", "Try to",
        "Consider", "Think about"
    ]
    
    for phrase in directive_phrases:
        response = response.replace(phrase, "")
    
    # Enforce max length
    if len(response) > 200:
        response = response[:197] + '...'
    
    return response.strip()
