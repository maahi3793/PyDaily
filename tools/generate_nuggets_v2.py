import os
import sys
import random
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager
from backend.curriculum import TOPICS
from tools import feed_templates
from dotenv import load_dotenv

load_dotenv()

def mock_ai_generate_v2(day, topic):
    """
    Mocking the AI Generation based on Topic.
    Returns a list of 3 nuggets (mixed types).
    """
    nuggets = []
    
    # helper
    def safe_topic(t): return t.split("(")[0].strip()
    
    clean_topic = safe_topic(topic)
    
    # 1. Gradient Fact/Tip
    nuggets.append({
        "type": "tip",
        "topic": clean_topic,
        "title": f"Did you know?",
        "content_html": feed_templates.render_gradient_card(
            clean_topic,
            "The Monty Python Connection",
            f"Python isn't named after a snake! It's named after the British comedy group Monty Python. Enjoy the humor in the docs! 🎪"
        ),
        "media_url": None,
        "score": 8
    })
    
    # 2. Code Snippet
    code_ex = f"items = ['apple', 'banana']\nfor x in items:\n    print(f'I love {{x}}')"
    nuggets.append({
        "type": "snippet",
        "topic": clean_topic,
        "title": f"Mastering {clean_topic}",
        "content_html": feed_templates.render_code_card(
            clean_topic,
            "Iterating Like a Pro",
            code_ex,
            "Use f-strings inside loops for clean, readable output processing."
        ),
        "media_url": None,
        "score": 9
    })
    
    # 3. Image Concept (Day 2 example)
    if day == 2 or day % 5 == 0:
        nuggets.append({
            "type": "image",
            "topic": clean_topic,
            "title": "Visualizing Memory",
            "content_html": feed_templates.render_image_card(
                clean_topic,
                "Variables are Boxes",
                "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&q=80", # Generic abstract
                f"Think of variables in {clean_topic} as containers that hold your data."
            ),
            "media_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&q=80",
            "score": 10
        })
        
    return nuggets

def save_nugget_v2(db, day, nugget):
    # Try to write to db
    # NOTE: The schema must match! Ensure you ran setup_feed.sql
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

def run_v2(start=1, end=5):
    print(f"🎬 Starting V2 Generator (Topic-Centric)...")
    db = SupabaseManager()
    
    for day in range(start, end+1):
        topic = TOPICS.get(day, "General Python")
        if "Quiz" in topic: continue
        
        print(f"Processing Day {day}: {topic}")
        nuggets = mock_ai_generate_v2(day, topic)
        
        for n in nuggets:
            try:
                save_nugget_v2(db, day, n)
                print(f"   ✅ Saved: {n['title']}")
            except Exception as e:
                print(f"   ❌ Failed to save: {e}")
                
    print("✨ V2 Generation Complete.")

def ensure_nuggets_for_day(day):
    """
    Called by run_bot.py to ensure nuggets exist for a specific day.
    Safe to call repeatedly (Idempotent).
    """
    db = SupabaseManager()
    
    # 1. Check if ANY nugget exists for this day
    try:
        res = db.supabase.table("feed_nuggets").select("id").eq("lesson_day", day).limit(1).execute()
        if res.data and len(res.data) > 0:
            return # Already exists
    except Exception as e:
        print(f"⚠️ [Feed Auto] Existence check failed: {e}")
        return

    # 2. Generate if missing
    topic = TOPICS.get(day, f"Day {day} Topic")
    
    # Skip Quizzes or Reviews if desired (optional)
    if "Quiz" in topic: return 
    
    print(f"⚡ [Feed Auto] Generating Missing Nuggets for Day {day}...")
    try:
        nuggets = mock_ai_generate_v2(day, topic)
        for n in nuggets:
            save_nugget_v2(db, day, n)
    except Exception as e:
        print(f"❌ [Feed Auto] Generation Failed: {e}")

if __name__ == "__main__":
    run_v2(1, 10)
