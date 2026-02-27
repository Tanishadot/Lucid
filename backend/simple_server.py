from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.simple_routes import router
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="LUCID Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the simple routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"status": "LUCID Backend Running", "message": "Pattern-based retrieval system active"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "retrieval": "pattern-based"}

if __name__ == "__main__":
    import uvicorn
    print("=== STARTING LUCID BACKEND ===")
    print("Using pattern-based retrieval system")
    print("Server starting on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
