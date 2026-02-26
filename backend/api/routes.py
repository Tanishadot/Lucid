from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from services.chat_service import ChatService, ChatRequest, ChatResponse, SessionInfo
from api.dependencies import get_chat_service


router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Process a chat message and get reflective response"""
    try:
        response = await chat_service.chat(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}", response_model=SessionInfo)
async def get_session_info(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Get information about a session"""
    session_info = await chat_service.get_session_info(session_id)
    if not session_info:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_info


@router.get("/session/{session_id}/history")
async def get_conversation_history(
    session_id: str,
    max_messages: int = 10,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Get conversation history for a session"""
    history = await chat_service.get_conversation_history(session_id, max_messages)
    return {"session_id": session_id, "history": history}


@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Delete a session"""
    success = await chat_service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}


@router.post("/session/{session_id}/clear")
async def clear_session(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Clear conversation history for a session"""
    success = await chat_service.clear_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session cleared successfully"}


@router.get("/sessions/count")
async def get_active_sessions_count(
    chat_service: ChatService = Depends(get_chat_service)
):
    """Get count of active sessions"""
    count = await chat_service.get_active_sessions_count()
    return {"active_sessions": count}


@router.get("/health")
async def health_check(
    chat_service: ChatService = Depends(get_chat_service)
):
    """Health check for all components"""
    health_status = await chat_service.health_check()
    return health_status


@router.get("/session/{session_id}/analyze")
async def analyze_session(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Analyze session for insights"""
    analysis = await chat_service.analyze_session(session_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Session not found")
    return analysis
