from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.simple_routes import router

app = FastAPI(title="LUCID Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup_event():
    print("=== LUCID BACKEND STARTUP ===")
    print("Server started successfully.")
    print("Chroma will initialize lazily on first request.")
    print("=== STARTUP COMPLETE ===")

@app.get("/")
def root():
    return {"message": "LUCID backend running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "chroma": "lazy-loading"}