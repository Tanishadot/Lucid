import requests
import json

# Test with debug info
response = requests.post(
    'http://localhost:8000/api/v1/reflect',
    json={
        'user_input': 'I feel like I am failing at everything lately',
        'session_id': 'test'
    }
)

print("=== TEST RESULT ===")
print("Status Code:", response.status_code)
print("Response:", response.json())
print("==================")

# Test simple pattern directly
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple_retrieval import simple_pattern_retrieval

print("\n=== DIRECT PATTERN TEST ===")
result = simple_pattern_retrieval("I feel like I am failing at everything lately")
print("Direct pattern result:", result)
