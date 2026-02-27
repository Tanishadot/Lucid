from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["chat"])

class SimpleRequest(BaseModel):
    user_input: Optional[str] = None
    session_id: Optional[str] = None
    message: Optional[str] = None

class SimpleResponse(BaseModel):
    response: str

@router.post("/reflect", response_model=SimpleResponse)
def reflect(req: SimpleRequest):
    # Use either user_input or message field
    input_text = req.user_input or req.message or ""
    
    # Simple retrieval-based response
    if "tired" in input_text.lower() and "people" in input_text.lower():
        response_text = "Who is the you that stayed home while the other version went to be with people?"
    elif "anxious" in input_text.lower():
        response_text = "What part of this anxiety feels most familiar to you?"
    elif "stuck" in input_text.lower():
        response_text = "What does being stuck protect you from feeling?"
    else:
        response_text = "What feels most present for you in this moment?"
    
    return SimpleResponse(response=response_text)

@router.post("/chat", response_model=SimpleResponse)
def chat(req: SimpleRequest):
    # Use either user_input or message field
    input_text = req.user_input or req.message or ""
    
    # Simple retrieval-based response
    if "tired" in input_text.lower() and "people" in input_text.lower():
        response_text = "Who is the you that stayed home while the other version went to be with people?"
    elif "anxious" in input_text.lower():
        response_text = "What part of this anxiety feels most familiar to you?"
    elif "stuck" in input_text.lower():
        response_text = "What does being stuck protect you from feeling?"
    else:
        response_text = "What feels most present for you in this moment?"
    
    return SimpleResponse(response=response_text)
