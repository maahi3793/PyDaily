import requests
import json

api_key = "AIzaSyDwIU6HsOz-VUuIRsbYThWz3-J21ZxMZE4"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    models = response.json().get('models', [])
    for m in models:
        print(m['name'])
except Exception as e:
    print(f"Error: {e}")
