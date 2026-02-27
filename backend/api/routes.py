from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from core.reflection_engine.engine import run_reflection

router = APIRouter(prefix="/api/v1", tags=["chat"])

class ReflectionRequest(BaseModel):
    user_input: Optional[str] = None
    session_id: Optional[str] = None
    message: Optional[str] = None

class ReflectionResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ReflectionResponse)
def chat(req: ReflectionRequest):
    result = run_reflection(req.user_input)
    return ReflectionResponse(response=result)

@router.post("/reflect", response_model=ReflectionResponse)
def reflect(req: ReflectionRequest):
    # Use either user_input or message field
    input_text = req.user_input or req.message or ""
    result = run_reflection(input_text)
    return ReflectionResponse(response=result)