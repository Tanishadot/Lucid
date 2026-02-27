import os
from openai import OpenAI

# Initialize client with fallback for missing API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

def call_llm(prompt: str, temperature: float = 0.2):
    if not client:
        # Fallback response when no API key is available
        return "What feels most present for you in this moment?"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM Error: {e}")
        return "What feels most present for you in this moment?"