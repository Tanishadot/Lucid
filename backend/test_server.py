import requests
import json

# Test the API endpoint
response = requests.post(
    'http://localhost:8000/api/v1/reflect',
    json={
        'user_input': 'I feel like I am failing at everything lately',
        'session_id': 'test'
    }
)

print("Status Code:", response.status_code)
print("Response:", response.json())
