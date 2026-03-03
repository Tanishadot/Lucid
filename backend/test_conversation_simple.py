"""
Simple conversation API test
"""
from fastapi import FastAPI
from config.database import AsyncSessionLocal
from sqlalchemy import text

app = FastAPI()

@app.get("/api/conversations")
async def get_conversations():
    """Simple test endpoint"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM conversations"))
            count = result.scalar()
            return [{"id": "test", "title": f"Test Conversation ({count})", "user_id": "test-user"}]
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/conversations/start")
async def start_conversation(data: dict):
    """Simple test endpoint"""
    try:
        return {"id": "test-id", "title": data.get("first_message", "No message"), "messages": []}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
