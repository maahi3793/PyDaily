import requests
import json

api_key = "AIzaSyDwIU6HsOz-VUuIRsbYThWz3-J21ZxMZE4"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"

headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{"parts":[{"text": "What is a variable?"}]}]
}

print("Pinging Gemini directly...")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
