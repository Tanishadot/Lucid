import requests
import json

# Test the API endpoint with the failing pattern
response = requests.post(
    'http://localhost:8000/api/v1/reflect',
    json={
        'user_input': 'I feel like I am failing at everything lately',
        'session_id': 'test'
    }
)

print("=== END-TO-END RETRIEVAL TEST ===")
print("Status Code:", response.status_code)
print("Response:", response.json())

# Test with another pattern
response2 = requests.post(
    'http://localhost:8000/api/v1/reflect',
    json={
        'user_input': 'I feel tired after being with people',
        'session_id': 'test'
    }
)

print("\nSecond Request Status:", response2.status_code)
print("Second Response:", response2.json())
