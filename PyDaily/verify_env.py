import os
import sys
from dotenv import load_dotenv

# Replicate the app's env loading
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
gemini = os.getenv("GEMINI_API_KEY")

print(f"SUPABASE_URL: {'[FOUND]' if url else '[MISSING]'}")
print(f"SUPABASE_KEY: {'[FOUND]' if key else '[MISSING]'}")
print(f"GEMINI_KEY: {'[FOUND]' if gemini else '[MISSING]'}")

try:
    from supabase import create_client
    if url and key:
        client = create_client(url, key)
        # Try a simple auth check
        print("Connecting to Supabase...")
        res = client.auth.get_user()
        print("Connection check successful (Auth client ready).")
except Exception as e:
    print(f"Error: {e}")
