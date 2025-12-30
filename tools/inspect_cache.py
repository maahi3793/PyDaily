import sys
import os
from dotenv import load_dotenv

# Load Env
load_dotenv()

# Add Parent Dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager
from backend.lesson_manager import LessonManager

def inspect_cache():
    print("🔍 Inspecting Day 3 Cache...")
    
    # 1. Check DB directly
    db = SupabaseManager()
    res = db.supabase.table('daily_content').select('*').eq('day', 3).execute()
    print(f"📊 DB 'daily_content' Day 3 Rows: {len(res.data)}")
    if res.data:
        print(f"   Row ID: {res.data[0].get('id')}")
        print(f"   Content Length: {len(res.data[0].get('content', ''))}")

    # 2. Check File System
    fpath = os.path.join("lessons", "day_3_lesson.html")
    exists = os.path.exists(fpath)
    print(f"📂 File '{fpath}' Exists: {exists}")
    if exists:
        print(f"   Size: {os.path.getsize(fpath)} bytes")

    # 3. Check Manager Logic
    mgr = LessonManager()
    val = mgr.get_lesson(3)
    print(f"🧠 LessonManager.get_lesson(3) Returns: {'[CONTENT FOUND]' if val else '[NONE]'}")
    if val:
        print(f"   Content Start: {val[:50]}...")

if __name__ == "__main__":
    inspect_cache()
