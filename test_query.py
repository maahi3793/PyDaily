import requests
import json

url = "http://localhost:8000/api/v1/query"

# Requires a real API key or mock in env. Assuming active DEV env.
data = {
    "query": "what is a variable?",
    "model": "gemini-2.0-flash"
}

print("Querying...")
response = requests.post(url, json=data)

print(response.status_code)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))
else:
    print(response.text)
