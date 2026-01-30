import os
import sys
import json
import time

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager
from dotenv import load_dotenv

# Load env for Supabase keys
load_dotenv()

def mock_llm_call(lesson_html, api_key):
    """
    PLACEHOLDER: This is where you call Gemini / OpenAI.
    Input: Lesson HTML
    Output: JSON List of 3 Viral Hooks
    """
    if not api_key:
        print("⚠️ No API Key provided. Using Mock Data.")
        
    # Example prompts you would send:
    # "Extract 3 educational hooks from this. 1 code snippet, 1 trap, 1 fact. Format as JSON."
    
    # Mock Response
    return [
        {
            "type": "code",
            "title": "Why list() consumes iterators",
            "content": "it = iter([1, 2, 3])\nprint(list(it)) # [1, 2, 3]\nprint(list(it)) # [] <- Empty!",
            "virality_score": 9
        },
        {
            "type": "trap",
            "title": "The Mutable Default Arg Trap",
            "content": "Never do `def func(x=[]):`. It keeps the list between calls! Python parses defaults only once.",
            "virality_score": 8
        },
        {
            "type": "fact",
            "title": "Python's secret 'Anti-Gravity'",
            "content": "Type `import antigravity` in your Python shell. Seriously. Go do it.",
            "virality_score": 10
        }
    ]

def save_nugget(db, day, nugget):
    """Saves a single nugget to the DB."""
    data = {
        "lesson_day": day,
        "type": nugget["type"],
        "title": nugget["title"],
        "content": nugget["content"],
        "virality_score": nugget.get("virality_score", 5)
    }
    
    # Supabase Insert (Must use Admin Client for Service Role RLS)
    client = db.admin_supabase if db.admin_supabase else db.supabase
    if not client:
        raise Exception("No Supabase Client available")
        
    res = client.table("feed_nuggets").insert(data).execute()
    return res

def run_generator(start_day=1, end_day=5, api_key=None):
    print(f"🚀 Starting Nugget Generator (Days {start_day}-{end_day})...")
    db = SupabaseManager()
    
    if not db.supabase:
        print("❌ Supabase connection failed. Check .env")
        return

    for day in range(start_day, end_day + 1):
        print(f"Processing Day {day}...")
        
        # 1. Fetch Lesson
        lesson_html = db.get_daily_content(day)
        
        if not lesson_html:
            print(f"   ⚠️ No lesson content found for Day {day}. Skipping.")
            continue
            
        # 2. Generate Nuggets (AI magic happens here)
        nuggets = mock_llm_call(lesson_html, api_key)
        
        # 3. Save to DB
        for i, nug in enumerate(nuggets):
            try:
                save_nugget(db, day, nug)
                print(f"   ✅ Saved Nugget {i+1}: {nug['title']}")
            except Exception as e:
                print(f"   ❌ Error saving nugget: {e}")
                
        time.sleep(1) # Be nice to the API

    print("\n🎉 DONE! Feed nuggets populated.")

if __name__ == "__main__":
    # You can pass API Key here
    # api_key = os.getenv("GEMINI_API_KEY") 
    run_generator(start_day=1, end_day=5, api_key=None)
