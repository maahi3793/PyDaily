import os
import sys
import time
import logging

# Path Setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend import lesson_manager, gemini_service, curriculum, config as config_loader
from backend.db_supabase import SupabaseManager

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def nuke_and_regenerate(start_day=4, end_day=100):
    print(f"☢️  INITIATING NUKE & REGEN PROTOCOL (Days {start_day}-{end_day}) ☢️")
    print("⏳ This will take substantial time (API Rate Limits).")
    
    # Init Config & Services
    config = config_loader.get_config()
    api_key = config.get('gemini_key')
    
    cache = lesson_manager.LessonManager()
    gemini = gemini_service.GeminiService(api_key)
    db = SupabaseManager()
    
    # 1. NUKE PHASE
    print("\n💥 DELETING OLD VISIONS (Deleting daily_content rows)...")
    try:
        # Supabase Delete: .delete().gte('day', start_day)
        res = db.admin_supabase.table('daily_content').delete().gte('day', start_day).execute()
        print(f"   -> Deleted {len(res.data) if res.data else 'Unknown'} rows.")
    except Exception as e:
        print(f"   ❌ Delete Failed (Method might be restricted?): {e}")
        # Proceed anyway, upsert will overwrite.

    # 2. REGEN PHASE
    print("\n🌱 REGENERATING TIMELINE...")
    
    for day in range(start_day, end_day + 1):
        topic = curriculum.TOPICS.get(day, f"Day {day} Concept")
        is_quiz_day = (day % 3 == 0)
        
        print(f"\n⚙️  Processing Day {day} | Topic: {topic} | QuizDay: {is_quiz_day}")
        
        try:
            # A. Lesson / Quiz Generation
            if is_quiz_day:
                # Generate Quiz
                history = cache.get_topics_history(day) # Include today(quiz) in history context? No, up to now.
                content = gemini.generate_quiz(day, history)
                # Save as Lesson (Quiz Content)
                cache.save_lesson(day, content)
                print("   -> ✅ Quiz Generated & Saved.")
            else:
                # Generate Lesson
                history = cache.get_topics_history(day - 1)
                phase, phase_goal = curriculum.get_phase_info(day)
                
                # STRICT CALL
                content = gemini.generate_lesson(day, topic, phase, phase_goal, history_context=history)
                cache.save_lesson(day, content)
                print("   -> ✅ Lesson Generated & Saved.")

            time.sleep(4) # Rate Limit

            # B. Reminder Generation
            rem_content = gemini.generate_reminder(day, topic_name=topic)
            
            # Fix Header if needed
            if f"Day {day}" not in rem_content:
                rem_content = f"<h3>🌙 Nightly Check-in: Day {day}</h3>\n" + rem_content
            
            cache.save_reminder(day, rem_content)
            print("   -> ✅ Reminder Generated & Saved.")
            
            time.sleep(4) # Rate Limit
            
        except Exception as e:
            print(f"   ❌ FAILED Day {day}: {e}")
            time.sleep(10)

    print("\n✨ UNIVERSE RESTORED. COMPLETED.")

if __name__ == "__main__":
    nuke_and_regenerate()
