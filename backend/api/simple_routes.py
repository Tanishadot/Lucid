from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import the retrieval system, fallback to simple pattern matching
try:
    from knowledge.vector_store.retriever import retrieve_reflection_unit
    from core.prompt_manager.prompt_builder import build_prompt
    from core.memory.memory_manager import store_interaction
    from core.llm.llm_client import call_llm, validate_response
    USE_VECTOR_STORE = True
    print("Using natural LLM generation with vector store")
except Exception as e:
    print(f"Vector store not available: {e}")
    from simple_retrieval import simple_pattern_retrieval
    USE_VECTOR_STORE = False
    print("Using pattern-based retrieval")

router = APIRouter(prefix="/api/v1", tags=["chat"])

class SimpleRequest(BaseModel):
    user_input: Optional[str] = None
    session_id: Optional[str] = None
    message: Optional[str] = None

class SimpleResponse(BaseModel):
    response: str

def process_with_natural_reasoning(input_text: str):
    """Process input with natural LLM reasoning"""
    if USE_VECTOR_STORE:
        # 1. Retrieve optional context (soft, no decisions)
        retrieval_context = retrieve_reflection_unit(input_text)
        
        # 2. Build prompt with optional hints
        prompt = build_prompt(input_text, retrieval_context)
        
        # 3. Always let the model generate
        raw_response = call_llm(prompt, temperature=0.2)
        
        # 4. Validate response constraints
        validated_response = validate_response(raw_response)
        
        # 5. Store interaction
        store_interaction(input_text, validated_response)
        
        return validated_response
    else:
        # Use pattern-based retrieval as fallback
        result = simple_pattern_retrieval(input_text)
        reframe = result.get("reframe", "")
        question = result.get("question", "")
        
        # Format response
        if reframe and question:
            response_text = f"{reframe} {question}"
        elif question:
            response_text = question
        else:
            response_text = "What feels most present for you in this moment?"
        
        # Store interaction
        store_interaction(input_text, response_text)
        
        return response_text

@router.post("/reflect", response_model=SimpleResponse)
def reflect(req: SimpleRequest):
    # Use either user_input or message field
    input_text = req.user_input or req.message or ""
    
    if not input_text:
        return SimpleResponse(response="What feels most present for you in this moment?")
    
    try:
        response_text = process_with_natural_reasoning(input_text)
        return SimpleResponse(response=response_text)
        
    except Exception as e:
        print(f"Error in reflection: {e}")
        return SimpleResponse(response="What feels most present for you in this moment?")

@router.post("/chat", response_model=SimpleResponse)
def chat(req: SimpleRequest):
    # Use either user_input or message field
    input_text = req.user_input or req.message or ""
    
    if not input_text:
        return SimpleResponse(response="What feels most present for you in this moment?")
    
    try:
        response_text = process_with_natural_reasoning(input_text)
        return SimpleResponse(response=response_text)
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return SimpleResponse(response="What feels most present for you in this moment?")
