"""
Minimal test to debug API issues
"""
from fastapi import FastAPI
from sqlalchemy import text
from config.database import AsyncSessionLocal

app = FastAPI()

@app.get("/test-db")
async def test_db():
    """Test database connection"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            return {"status": "ok", "result": "Database connection works"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/test-simple")
async def test_simple():
    """Simple test endpoint"""
    return {"status": "ok", "message": "Simple test works"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
