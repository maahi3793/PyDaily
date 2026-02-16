import os
import sys
import logging

# Add parent path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager
from backend.gemini_service import GeminiService
from backend.curriculum import TOPICS

# Load Config
import json
try:
    with open('config.json') as f:
        config = json.load(f)
        GEMINI_KEY = config.get("gemini_key")
except:
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def regenerate_days():
    print("🔄 Starting Boss Battle Regeneration for Days 4 & 5...")
    
    if not GEMINI_KEY:
        print("❌ Gemini Key Missing")
        return

    db = SupabaseManager()
    gemini = GeminiService(GEMINI_KEY)
    
    days_to_fix = [4, 5]
    
    for day in days_to_fix:
        print(f"\n--- Processing Day {day} ---")
        
        # 1. Delete Existing (Forcefully)
        print(f"🗑️ Deleting existing battles for Day {day}...")
        try:
            # Check count before
            pre_check = db.supabase.table('boss_battles').select('*', count='exact').eq('day', day).execute()
            print(f"   Found {pre_check.count} existing rows.")
            
            # Delete
            db.supabase.table('boss_battles').delete().eq('day', day).execute()
            
            # Verify Delete
            post_check = db.supabase.table('boss_battles').select('*', count='exact').eq('day', day).execute()
            if post_check.count > 0:
                print(f"❌ Deletion Failed! Still has {post_check.count} rows. Aborting generation.")
                continue
            
            print("   ✅ Cleaned successfully.")
        except Exception as e:
            print(f"⚠️ Deletion Error: {e}")
            continue

        # 2. Get Topic
        topic = TOPICS.get(day, "Python Basics")
        print(f"📚 Topic: {topic}")
        
        # 3. Generate New Battles (Now 5, Toned Down)
        print(f"🧠 Generating 5 Job-Ready Battles...")
        battles = gemini.generate_boss_battles(topic, day)
        
        if battles:
            # 4. Save
            result = db.save_boss_battles(day, topic, battles)
            if result:
                print(f"✅ Generated & Saved {len(battles)} Battles for Day {day}.")
            else:
                print(f"❌ Failed to Save Day {day}.")
        else:
            print(f"❌ Generation Failed for Day {day}.")

    print("\n✨ Regeneration Complete.")

if __name__ == "__main__":
    regenerate_days()
