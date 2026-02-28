"""
Database initialization script for LUCID conversations
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.database import ASYNC_DATABASE_URL
from models.conversation import Base
import os
from dotenv import load_dotenv

load_dotenv()

async def init_database():
    """Initialize database tables"""
    print("=== Initializing Database ===")
    
    # Create async engine
    engine = create_async_engine(
        ASYNC_DATABASE_URL,
        echo=os.getenv("DEBUG", "false").lower() == "true"
    )
    
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Database tables created successfully")
            
        # Test connection
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            # Simple test query
            result = await session.execute("SELECT 1")
            print("✅ Database connection test passed")
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    finally:
        await engine.dispose()
    
    print("=== Database initialization complete ===")

if __name__ == "__main__":
    asyncio.run(init_database())
