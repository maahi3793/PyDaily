import sys
import os

sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend.gemini_service import GeminiService

api_key = "dummy"
with open('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily/.env', 'r') as f:
    for line in f:
        if 'GEMINI_API_KEY' in line:
            api_key = line.split('=')[1].strip().strip('"').strip("'")
            break

gemini = GeminiService(api_key)
print("Testing Reminder Generation for Day 43...")
content = gemini.generate_reminder(43, "File I/O: Writing and Appending to files", "Context Managers (The with statement)")
print("=== RESULT ===")
print(content)
print(f"Length: {len(content)}")
