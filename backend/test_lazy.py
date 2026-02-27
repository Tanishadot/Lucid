import requests
import json

# Test the API endpoint to trigger lazy loading
print("=== TESTING LAZY CHROMA INITIALIZATION ===")

# First request should trigger lazy loading
response1 = requests.post(
    'http://localhost:8000/api/v1/reflect',
    json={
        'user_input': 'I feel like I am failing at everything lately',
        'session_id': 'test'
    }
)

print("First Request Status:", response1.status_code)
print("First Request Response:", response1.json())

# Second request should use cached Chroma
response2 = requests.post(
    'http://localhost:8000/api/v1/reflect',
    json={
        'user_input': 'I feel tired after being with people',
        'session_id': 'test'
    }
)

print("\nSecond Request Status:", response2.status_code)
print("Second Request Response:", response2.json())

print("\n=== LAZY LOADING TEST COMPLETE ===")
