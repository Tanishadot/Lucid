from fastapi import APIRouter, File, UploadFile, HTTPException
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

class TranscriptionResponse(BaseModel):
    transcript: str

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

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio file using a mock implementation.
    In production, this would integrate with OpenAI Whisper or similar service.
    """
    try:
        # Check file type
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read file content (for demo purposes, we'll mock transcription)
        audio_content = await file.read()
        
        # Mock transcription - in production, use OpenAI Whisper or similar
        # For now, return a placeholder response
        mock_transcript = "This is a mock transcription. In production, this would be the actual transcribed text from your audio."
        
        print(f"Received audio file: {file.filename}, size: {len(audio_content)} bytes")
        print(f"Content type: {file.content_type}")
        
        return TranscriptionResponse(transcript=mock_transcript)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in transcription: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed")

# Add the transcribe endpoint to the main API path as well
@router.post("/api/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio_main(file: UploadFile = File(...)):
    """Alternative path for transcription endpoint"""
    return await transcribe_audio(file)
