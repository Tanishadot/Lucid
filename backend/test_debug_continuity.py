import requests
import json

def test_debugged_continuity():
    """Test debugged cognitive continuity with detailed logging"""
    base_url = "http://localhost:8000/api/v1"
    
    print("=== TESTING DEBUGGED COGNITIVE CONTINUITY ===")
    
    # Turn 1: Establish pattern
    print("\n--- TURN 1: ESTABLISHING PATTERN ---")
    response1 = requests.post(f"{base_url}/reflect", json={
        "user_input": "I feel like I am failing at everything lately",
        "session_id": "debug_test"
    })
    
    print(f"Status: {response1.status_code}")
    result1 = response1.json()
    print(f"Response: {result1['response']}")
    
    # Turn 2: Should continue pattern
    print("\n--- TURN 2: CONTINUING PATTERN ---")
    response2 = requests.post(f"{base_url}/reflect", json={
        "user_input": "If I separate worth from success, isn't it still failure?",
        "session_id": "debug_test"
    })
    
    print(f"Status: {response2.status_code}")
    result2 = response2.json()
    print(f"Response: {result2['response']}")
    
    # Turn 3: Should deepen same pattern
    print("\n--- TURN 3: DEEPENING PATTERN ---")
    response3 = requests.post(f"{base_url}/reflect", json={
        "user_input": "What do I do about this feeling?",
        "session_id": "debug_test"
    })
    
    print(f"Status: {response3.status_code}")
    result3 = response3.json()
    print(f"Response: {result3['response']}")
    
    # Turn 4: Different topic - potential shift
    print("\n--- TURN 4: DIFFERENT TOPIC ---")
    response4 = requests.post(f"{base_url}/reflect", json={
        "user_input": "I feel exhausted after social interactions",
        "session_id": "debug_test"
    })
    
    print(f"Status: {response4.status_code}")
    result4 = response4.json()
    print(f"Response: {result4['response']}")
    
    print("\n=== DEBUGGED CONTINUITY TEST COMPLETE ===")
    print("Check server logs for detailed debugging information")

if __name__ == "__main__":
    test_debugged_continuity()
