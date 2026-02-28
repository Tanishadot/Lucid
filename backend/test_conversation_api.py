"""
Test script for conversation API endpoints
"""
import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_conversation_api():
    """Test all conversation API endpoints"""
    print("=== Testing Conversation API ===")
    
    async with httpx.AsyncClient() as client:
        try:
            # Test 1: Get conversations (should be empty initially)
            print("\n1. Testing GET /api/conversations")
            response = await client.get(f"{BASE_URL}/api/conversations")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            # Test 2: Start a new conversation
            print("\n2. Testing POST /api/conversations/start")
            start_data = {"first_message": "Hello, this is my first message"}
            response = await client.post(
                f"{BASE_URL}/api/conversations/start",
                json=start_data
            )
            print(f"Status: {response.status_code}")
            conversation_data = response.json()
            print(f"Response: {json.dumps(conversation_data, indent=2, default=str)}")
            
            conversation_id = conversation_data.get("id")
            if not conversation_id:
                print("❌ No conversation ID returned")
                return
            
            # Test 3: Get the specific conversation
            print(f"\n3. Testing GET /api/conversations/{conversation_id}")
            response = await client.get(f"{BASE_URL}/api/conversations/{conversation_id}")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
            
            # Test 4: Add a message to the conversation
            print(f"\n4. Testing POST /api/conversations/{conversation_id}/messages")
            message_data = {
                "conversation_id": conversation_id,
                "role": "user",
                "content": "This is a follow-up message"
            }
            response = await client.post(
                f"{BASE_URL}/api/conversations/{conversation_id}/messages",
                json=message_data
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
            
            # Test 5: Add an assistant message
            print(f"\n5. Testing POST /api/conversations/{conversation_id}/messages (assistant)")
            message_data = {
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": "I understand. Tell me more about that."
            }
            response = await client.post(
                f"{BASE_URL}/api/conversations/{conversation_id}/messages",
                json=message_data
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
            
            # Test 6: Get conversations again (should show our conversation)
            print("\n6. Testing GET /api/conversations (after creating)")
            response = await client.get(f"{BASE_URL}/api/conversations")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
            
            # Test 7: Get conversation with all messages
            print(f"\n7. Testing GET /api/conversations/{conversation_id} (final)")
            response = await client.get(f"{BASE_URL}/api/conversations/{conversation_id}")
            print(f"Status: {response.status_code}")
            final_data = response.json()
            print(f"Response: {json.dumps(final_data, indent=2, default=str)}")
            
            print("\n✅ All API tests completed successfully!")
            
        except httpx.ConnectError:
            print("❌ Could not connect to the server. Make sure the backend is running on localhost:8000")
        except Exception as e:
            print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(test_conversation_api())
