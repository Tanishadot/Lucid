import requests
import json

def test_clean_architecture():
    """Test the clean LUCID architecture with user dilemmas"""
    base_url = "http://localhost:8000/api/v1"
    
    print("=== TESTING CLEAN LUCID ARCHITECTURE ===")
    
    # Test dilemmas
    test_cases = [
        "I feel like I'm a bad person because I keep making selfish choices",
        "I'm struggling with whether to quit my job to pursue my passion",
        "I don't know if I should tell my friend the truth about their partner cheating",
        "I feel guilty about not spending enough time with my aging parents",
        "I'm torn between staying in my comfort zone and taking a big risk"
    ]
    
    for i, dilemma in enumerate(test_cases, 1):
        print(f"\n--- TEST CASE {i} ---")
        print(f"User Dilemma: {dilemma}")
        
        try:
            response = requests.post(f"{base_url}/reflect", json={
                "user_input": dilemma,
                "session_id": f"test_{i}"
            })
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"LUCID Response: {result['response']}")
                
                # Validate response constraints
                resp_text = result['response']
                question_count = resp_text.count('?')
                has_advice = any(phrase in resp_text.lower() for phrase in ['you should', 'try to', 'it may help'])
                has_reassurance = any(phrase in resp_text.lower() for phrase in ['it\'s okay', 'don\'t worry', 'that\'s normal'])
                
                print(f"✅ Question Count: {question_count}")
                print(f"✅ Contains Advice: {has_advice}")
                print(f"✅ Contains Reassurance: {has_reassurance}")
                
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n=== CLEAN ARCHITECTURE TEST COMPLETE ===")

if __name__ == "__main__":
    test_clean_architecture()
