import os
import sys

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager
from backend.gemini_service import GeminiService

# Load Config
import json
try:
    with open('config.json') as f:
        config = json.load(f)
        GEMINI_KEY = config.get("gemini_key")
except:
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def manual_gen(day, topic):
    print(f"⚔️ Manual Generation for Day {day} ({topic})...")
    
    if not GEMINI_KEY:
        print("❌ Gemini Key Missing")
        return

    db = SupabaseManager()
    gemini = GeminiService(GEMINI_KEY)
    
    battles = gemini.generate_boss_battles(topic, day)
    
    if battles:
        db.save_boss_battles(day, topic, battles)
        print("✅ Success.")
    else:
        print("❌ Failed.")

if __name__ == "__main__":
    # Day 4: Arithmetic
    manual_gen(4, "Basic Arithmetic")
