import requests
import json

# Test the API endpoint
response = requests.post(
    'http://localhost:8000/api/v1/reflect',
    json={
        'user_input': 'I feel tired after being with people',
        'session_id': 'test'
    }
)

print("Status Code:", response.status_code)
print("Response:", response.json())
