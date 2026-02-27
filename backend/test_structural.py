import requests
import json

def test_structural_interrogation():
    base_url = "http://localhost:8003/api/v1"
    
    print("=== TESTING DECLARATIVE STRUCTURAL INTERROGATION ===")
    
    test_cases = [
        "I feel like a failure",
        "I think I am introvert", 
        "I am not as good as my peers",
        "I hurt someone accidentally",
        "I make selfish decisions so I'm a bad person"
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- TEST {i} ---")
        print(f"User: {case}")
        
        try:
            response = requests.post(f"{base_url}/reflect", json={
                "user_input": case,
                "session_id": f"test_{i}"
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"LUCID: {result['response']}")
                
                # Check for structural vs interpretive patterns
                resp = result['response'].lower()
                has_forbidden_opening = any(p in resp for p in ["it sounds like", "it seems", "you seem to", "you are experiencing", "the situation"])
                has_forbidden_question = any(p in resp for p in ["what feelings arise", "why do you think", "what caused"])
                has_structural_keyword = any(p in resp for p in ["identity", "category", "definition", "standard", "assumption", "responsible", "comparison"])
                
                print(f"✅ No forbidden opening: {not has_forbidden_opening}")
                print(f"✅ No forbidden question: {not has_forbidden_question}")
                print(f"✅ Has structural keyword: {has_structural_keyword}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_structural_interrogation()
