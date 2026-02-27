from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.simple_routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("=== LUCID BACKEND STARTUP ===")
    print("Server started successfully.")
    print("Chroma will initialize lazily on first request.")
    print("=== STARTUP COMPLETE ===")
    
    yield
    
    # Shutdown
    print("=== LUCID BACKEND SHUTDOWN ===")


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

@app.get("/")
def root():
    return {"message": "LUCID backend running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "chroma": "lazy-loading"}