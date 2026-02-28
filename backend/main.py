from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.simple_routes import router, TranscriptionResponse
from api.conversation_routes import router as conversation_router
from config.database import async_engine
from models.conversation import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("=== LUCID BACKEND STARTUP ===")
    
    # Create database tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully.")
    
    print("Server started successfully.")
    print("Chroma will initialize lazily on first request.")
    print("=== STARTUP COMPLETE ===")
    
    yield
    
    # Shutdown
    print("=== LUCID BACKEND SHUTDOWN ===")
    await async_engine.dispose()


app = FastAPI(title="LUCID Backend", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(conversation_router)

@app.post("/api/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio_main(file: UploadFile = File(...)):
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

@app.get("/")
def root():
    return {"message": "LUCID backend running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "chroma": "lazy-loading"}