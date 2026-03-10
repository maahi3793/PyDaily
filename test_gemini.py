import sys
import os
sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend.gemini_service import GeminiService

import traceback

gemini = GeminiService("AIzaSyBwdfDffEsIvhfjKyIGvFaT_xvTWTlQ9")  # Placeholder dummy key, wait I'll use the one from env
# Actually I'll read it from the .env directly in Python to be safe.
with open('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily/.env', 'r') as f:
    for line in f:
        if 'GEMINI_API_KEY' in line:
            api_key = line.split('=')[1].strip().strip('"').strip("'")
            break

gemini = GeminiService(api_key)
print("Testing Reminder Generation for Day 43...")
try:
    content = gemini.generate_reminder(43, "File I/O: Writing and Appending to files", "Context Managers (The with statement)")
    print("=== RESULT ===")
    print(content)
except Exception as e:
    print(f"FAILED: {e}")
    traceback.print_exc()
