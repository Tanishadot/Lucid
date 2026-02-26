from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

from reflection_engine import ReflectionEngine
from safety_layer import SafetyLayer
from memory import MemoryManager

router = APIRouter()

class ReflectRequest(BaseModel):
    session_id: str
    message: str

class ReflectResponse(BaseModel):
    reflection: str
    metadata: dict

reflection_engine = ReflectionEngine()
safety_layer = SafetyLayer()
memory_manager = MemoryManager()

@router.post("/reflect", response_model=ReflectResponse)
async def reflect(request: ReflectRequest):
    try:
        # Safety check
        safety_result = safety_layer.check_message(request.message)
        if safety_result.requires_redirection:
            return ReflectResponse(
                reflection=safety_result.redirect_response,
                metadata={"safety_redirect": True}
            )
        
        # Store user message in memory
        memory_manager.add_message(request.session_id, request.message, is_user=True)
        
        # Generate reflection
        reflection = reflection_engine.generate_reflection(
            message=request.message,
            session_context=memory_manager.get_session_context(request.session_id)
        )
        
        # Store reflection in memory
        memory_manager.add_message(request.session_id, reflection, is_user=False)
        
        # Generate metadata (internal only)
        metadata = reflection_engine.analyze_message(request.message)
        
        return ReflectResponse(
            reflection=reflection,
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    try:
        session_data = memory_manager.get_session_context(session_id)
        return {"session_id": session_id, "messages": session_data}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session not found")

@router.post("/session")
async def create_session():
    session_id = str(uuid.uuid4())
    memory_manager.create_session(session_id)
    return {"session_id": session_id}
