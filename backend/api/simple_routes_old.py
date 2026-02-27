from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from core.reflection_engine import run_reflection

router = APIRouter(prefix="/api/v1", tags=["chat"])

class SimpleRequest(BaseModel):
    user_input: str
    session_id: Optional[str] = None
    message: Optional[str] = None

class SimpleResponse(BaseModel):
    response: str

def process_reflection(input_text: str):
    """Process input with clean reflection architecture"""
    return run_reflection(input_text)

@router.post("/reflect", response_model=SimpleResponse)
def reflect(req: SimpleRequest):
    # Use either user_input or message field
    input_text = req.user_input or req.message or ""
    
    if not input_text:
        return SimpleResponse(response="What feels most present for you in this moment?")
    
    try:
        response_text = process_reflection(input_text)
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
        response_text = process_reflection(input_text)
        return SimpleResponse(response=response_text)
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return SimpleResponse(response="What feels most present for you in this moment?")
