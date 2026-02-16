import os
import sys
import time
import logging

# Path Setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend import lesson_manager, gemini_service, curriculum, config as config_loader

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def regenerate_reminders(start_day=4, end_day=100):
    print(f"🚀 Starting Reminder Regeneration (Days {start_day}-{end_day})...")
    print("⏳ This will take time due to API Rate Limits (5s delay/req).")
    
    # Init Config
    config = config_loader.get_config()
    api_key = config.get('gemini_key')
    
    # Init Services
    cache = lesson_manager.LessonManager()
    gemini = gemini_service.GeminiService(api_key)
    
    for day in range(start_day, end_day + 1):
        # 1. Get Topic
        topic = curriculum.TOPICS.get(day, "Python Concepts")
        print(f"\nProcessing Day {day} (Topic: {topic})...")
        
        try:
            # 2. Generate
            content = gemini.generate_reminder(day, topic_name=topic)
            
            # 3. Validation/Fix Header (Just in case)
            if f"Day {day}" not in content:
                content = f"<h3>🌙 Nightly Check-in: Day {day}</h3>\n" + content
            
            # 4. Save
            cache.save_reminder(day, content)
            print(f"✅ Saved Day {day}.")
            
            # 5. Rate Limit Sleep
            time.sleep(5) 
            
        except Exception as e:
            print(f"❌ Failed Day {day}: {e}")
            time.sleep(10) # Longer sleep on error

    print("\n✨ Regeneration Complete!")

if __name__ == "__main__":
    regenerate_reminders()
