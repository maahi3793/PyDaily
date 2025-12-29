import sys
import os
from dotenv import load_dotenv

# Load Env
load_dotenv()

# Add Parent Dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager
from backend.gemini_service import GeminiService
from backend.lesson_manager import LessonManager
from backend.data_manager import get_config

def backfill_lessons():
    print("🔄 Starting Lesson Backfill (Day 1 & 2)...")
    
    config = get_config()
    key = config.get('gemini_key')
    if not key:
        print("❌ Gemini Key Missing.")
        return

    gemini = GeminiService(key)
    cache = LessonManager() # Uses DB internally now
    
    days_to_fix = [1, 2]
    
    for day in days_to_fix:
        # Check if exists
        existing = cache.get_lesson(day)
        if existing:
            print(f"✅ Day {day} already exists in DB/Cache. Skipping.")
            continue
            
        print(f"⚠️ Day {day} Missing. Regenerating...")
        
        # Topic context (simplified for backfill)
        history = "None" if day == 1 else "Day 1: Basic Printing"
        
        # Generate
        try:
             # Just generic phase info
            content = gemini.generate_lesson(day, history, "Phase 1: Basics", "Master syntax")
            
            # Save (This triggers DB save)
            cache.save_lesson(day, content)
            print(f"✅ Day {day} Regenerated and Saved to DB.")
            
        except Exception as e:
            print(f"❌ Failed to regen Day {day}: {e}")

if __name__ == "__main__":
    backfill_lessons()
