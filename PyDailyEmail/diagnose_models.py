import google.generativeai as genai
import json
import os

# Load config to get key
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        api_key = config.get('gemini_key')
except Exception as e:
    print(f"Could not read config.json: {e}")
    exit(1)

if not api_key:
    print("No API Key found in config.json")
    exit(1)

genai.configure(api_key=api_key)

with open('models.txt', 'w') as f:
    f.write("Listing available models:\n")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"- {m.name}\n")
    except Exception as e:
        f.write(f"Error listing models: {str(e)}\n")
print("Done writing to models.txt")
