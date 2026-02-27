import requests
import json

def test_natural_reasoning():
    """Test simplified natural reasoning architecture"""
    base_url = "http://localhost:8000/api/v1"
    
    print("=== TESTING NATURAL REASONING ARCHITECTURE ===")
    
    # Turn 1: Natural start
    print("\n--- TURN 1: NATURAL START ---")
    response1 = requests.post(f"{base_url}/reflect", json={
        "user_input": "I feel like I am a horrible person",
        "session_id": "natural_test"
    })
    
    print(f"Status: {response1.status_code}")
    result1 = response1.json()
    print(f"Response: {result1['response']}")
    
    # Turn 2: Natural continuation
    print("\n--- TURN 2: NATURAL CONTINUATION ---")
    response2 = requests.post(f"{base_url}/reflect", json={
        "user_input": "Because I hurt people sometimes",
        "session_id": "natural_test"
    })
    
    print(f"Status: {response2.status_code}")
    result2 = response2.json()
    print(f"Response: {result2['response']}")
    
    # Turn 3: Natural deepening
    print("\n--- TURN 3: NATURAL DEEPENING ---")
    response3 = requests.post(f"{base_url}/reflect", json={
        "user_input": "What do I do?",
        "session_id": "natural_test"
    })
    
    print(f"Status: {response3.status_code}")
    result3 = response3.json()
    print(f"Response: {result3['response']}")
    
    # Turn 4: Topic shift
    print("\n--- TURN 4: TOPIC SHIFT ---")
    response4 = requests.post(f"{base_url}/reflect", json={
        "user_input": "I feel exhausted after social interactions",
        "session_id": "natural_test"
    })
    
    print(f"Status: {response4.status_code}")
    result4 = response4.json()
    print(f"Response: {result4['response']}")
    
    print("\n=== NATURAL REASONING TEST COMPLETE ===")
    print("Expected: Natural flow, no mechanical pattern reuse, one question each")

if __name__ == "__main__":
    test_natural_reasoning()
