import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from google import genai
from dotenv import load_dotenv

# Load key from .env (PyDaily/.env)
load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env")
    exit(1)

client = genai.Client(api_key=api_key)
models_to_test = [
    'gemini-2.0-flash-exp', 
    'gemini-1.5-flash', 
    'gemini-1.5-flash-8b', 
    'gemini-1.5-pro'
]

print(f"🚀 Testing Gemini Models (Free Tier Connection Test)...")
print("-" * 50)

for m in models_to_test:
    print(f"Testing {m}...", end=" ", flush=True)
    try:
        # Simple JSON Test
        response = client.models.generate_content(
            model=m,
            contents="Return a JSON with a single key 'status' and value 'ok'."
        )
        txt = response.text.lower()
        if "ok" in txt:
            print(f"✅ SUCCESS!")
        else:
            print(f"⚠️ PARTIAL (Returned unexpected text: {response.text[:30]}...)")
    except Exception as e:
        # Check specifically for 404 vs Auth vs Quota
        err_msg = str(e)
        if "404" in err_msg:
            print(f"❌ 404 NOT FOUND")
        elif "429" in err_msg:
            print(f"❌ 429 QUOTA EXHAUSTED")
        else:
            print(f"❌ FAILED: {err_msg[:50]}...")

print("-" * 50)
print("Diagnostic complete.")
