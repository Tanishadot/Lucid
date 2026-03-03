"""
Debug script for conversation API
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import AsyncSessionLocal
from services.conversation_service import ConversationService

async def debug_conversation_service():
    """Debug the conversation service"""
    print("=== Debugging Conversation Service ===")
    
    try:
        async with AsyncSessionLocal() as db:
            service = ConversationService(db)
            
            # Test getting conversations
            print("Testing get_conversations_for_user...")
            conversations = await service.get_conversations_for_user("550e8400-e29b-41d4-a716-446655440000")
            print(f"✅ Got {len(conversations)} conversations")
            
            # Test creating a conversation
            print("Testing create_conversation...")
            from services.conversation_service import ConversationCreate
            conv_data = ConversationCreate(
                user_id="550e8400-e29b-41d4-a716-446655440000",
                title="Test Conversation"
            )
            conversation = await service.create_conversation(conv_data)
            print(f"✅ Created conversation: {conversation.id}")
            
            # Test getting conversations again
            print("Testing get_conversations_for_user again...")
            conversations = await service.get_conversations_for_user("550e8400-e29b-41d4-a716-446655440000")
            print(f"✅ Got {len(conversations)} conversations")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_conversation_service())
