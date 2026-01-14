import os
import sys
import logging
from datetime import datetime

# Setup Logging
logging.basicConfig(
    filename='pydaily_boss.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add parent path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db_supabase import SupabaseManager
from backend.gemini_service import GeminiService
from backend.curriculum import TOPICS as PYTHON_CURRICULUM

# Load Config
import json
try:
    with open('config.json') as f:
        config = json.load(f)
        GEMINI_KEY = config.get("gemini_key")
except:
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_boss_cycle():
    """
    Checks what days are active for students, and ensures Boss Battles exist for them.
    Runs separately from the main email cycle.
    """
    logging.info("🔥 Starting Boss Battle Cycle...")
    print("🔥 Starting Boss Battle Cycle...")

    if not GEMINI_KEY:
        print("❌ Gemini Key Missing")
        return

    db = SupabaseManager()
    gemini = GeminiService(GEMINI_KEY)
    
    # 1. Find which days are needed
    # We don't want to generate for Day 100 if no one is there.
    students = db.admin_get_all_students()
    if not students:
        print("No students found.")
        return

    active_days = set()
    for s in students:
        # We only care about students roughly in the flow
        day = s.get('day', 1)
        active_days.add(day)
    
    print(f"👥 Active Student Days: {sorted(list(active_days))}")
    
    # 2. Check and Generate
    for day in active_days:
        # Check if battles exist
        existing = db.get_boss_battles(day)
        if existing:
            print(f"✅ Day {day} already has {len(existing)} Battles.")
            continue
            
        print(f"⚔️ Generating Battles for Day {day}...")
        
        # Get Topic
        topic = PYTHON_CURRICULUM.get(day, "Advanced Python")
        
        # Call Gemini
        battles = gemini.generate_boss_battles(topic)
        
        if battles:
            # Save
            result = db.save_boss_battles(day, topic, battles)
            if result:
                print(f"✅ Saved Day {day}.")
            else:
                print(f"❌ Failed to Save Day {day}.")
        else:
            print(f"⚠️ Generation Failed for Day {day}.")
            
    print("🔥 Boss Cycle Complete.")

if __name__ == "__main__":
    run_boss_cycle()
