import os
import sys
import random
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager
from backend.curriculum import TOPICS
from tools import feed_templates
from tools.static_feed_content import STATIC_NUGGETS
from dotenv import load_dotenv

load_dotenv()

def mock_ai_generate_v2(day, topic):
    """
    Returns Static Content if available.
    """
    if day in STATIC_NUGGETS:
        return STATIC_NUGGETS[day]
    
    # Fallback if day not in static (shouldn't happen for 1-22)
    return []

def save_nugget_v2(db, day, nugget):
    # Try to write to db
    data = {
        "lesson_day": day,
        "topic": nugget["topic"],
        "type": nugget["type"],
        "title": nugget["title"],
        "content": nugget["content_html"], # Saving HTML directly
        "media_url": nugget.get("media_url"),
        "virality_score": nugget.get("score", 5)
    }
    
    client = db.admin_supabase if db.admin_supabase else db.supabase
    if not client: raise Exception("No Client")
    
    client.table("feed_nuggets").insert(data).execute()

def run_v2(start=1, end=22):
    print(f"🎬 Starting Static Seeder (Days {start}-{end})...")
    db = SupabaseManager()
    
    for day in range(start, end+1):
        # Check if we have static content
        nuggets = mock_ai_generate_v2(day, "")
        
        if not nuggets:
            print(f"⏩ Day {day}: No static content. Skipping.")
            continue
            
        print(f"Processing Day {day}...")
        
        for n in nuggets:
            try:
                save_nugget_v2(db, day, n)
                print(f"   ✅ Saved: {n['title']}")
            except Exception as e:
                print(f"   ❌ Failed to save: {e}")
                
    print("✨ Static Seeding Complete.")

def ensure_nuggets_for_day(day):
    """
    Called by run_bot.py. 
    If content exists in Static Library, use it.
    """
    db = SupabaseManager()
    
    # 1. Check if ANY nugget exists for this day
    try:
        res = db.supabase.table("feed_nuggets").select("id").eq("lesson_day", day).limit(1).execute()
        if res.data and len(res.data) > 0:
            return # Already exists
    except Exception as e:
        pass

    # 2. Generate if missing (using Static Lib)
    nuggets = mock_ai_generate_v2(day, "")
    if nuggets:
        print(f"⚡ [Feed Auto] Seeding Day {day} from Static Lib...")
        for n in nuggets:
            try:
                save_nugget_v2(db, day, n)
            except: pass

if __name__ == "__main__":
    run_v2(1, 22)
