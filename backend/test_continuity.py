import requests
import json

def test_cognitive_continuity():
    """Test cognitive continuity across multiple turns"""
    base_url = "http://localhost:8000/api/v1"
    
    print("=== TESTING COGNITIVE CONTINUITY ===")
    
    # First message - should establish pattern
    print("\n1. First message - establishing pattern:")
    response1 = requests.post(f"{base_url}/reflect", json={
        "user_input": "I feel like I am failing at everything lately",
        "session_id": "test"
    })
    
    print(f"Status: {response1.status_code}")
    result1 = response1.json()
    print(f"Response: {result1['response']}")
    
    # Second message - should continue same pattern
    print("\n2. Second message - continuing pattern:")
    response2 = requests.post(f"{base_url}/reflect", json={
        "user_input": "If I separate worth from success, isn't it still failure?",
        "session_id": "test"
    })
    
    print(f"Status: {response2.status_code}")
    result2 = response2.json()
    print(f"Response: {result2['response']}")
    
    # Third message - should deepen within same pattern
    print("\n3. Third message - deepening pattern:")
    response3 = requests.post(f"{base_url}/reflect", json={
        "user_input": "What do I do about this?",
        "session_id": "test"
    })
    
    print(f"Status: {response3.status_code}")
    result3 = response3.json()
    print(f"Response: {result3['response']}")
    
    # Fourth message - different topic, should potentially shift
    print("\n4. Fourth message - different topic:")
    response4 = requests.post(f"{base_url}/reflect", json={
        "user_input": "I feel tired after being with people all day",
        "session_id": "test"
    })
    
    print(f"Status: {response4.status_code}")
    result4 = response4.json()
    print(f"Response: {result4['response']}")
    
    print("\n=== COGNITIVE CONTINUITY TEST COMPLETE ===")

if __name__ == "__main__":
    test_cognitive_continuity()
