from fastapi import APIRouter
from pydantic import BaseModel
from core.reflection_engine.engine import run_reflection

router = APIRouter()

class ReflectionRequest(BaseModel):
    user_input: str

class ReflectionResponse(BaseModel):
    response: str

@router.post("/reflect", response_model=ReflectionResponse)
def reflect(req: ReflectionRequest):
    result = run_reflection(req.user_input)
    return ReflectionResponse(response=result)