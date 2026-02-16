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

def generate_day_6():
    day = 6
    print(f"🎯 Generatng Day {day} (Quiz Day)...")
    
    # Init Config & Services
    config = config_loader.get_config()
    api_key = config.get('gemini_key')
    
    cache = lesson_manager.LessonManager()
    gemini = gemini_service.GeminiService(api_key)
    
    # 1. Generate Quiz (Lesson Content)
    print("Generating Quiz...")
    history = cache.get_topics_history(day)
    content = gemini.generate_quiz(day, history)
    
    # Save with Explicit Topic
    topic_name = "Day 6 Quiz (Checkpoint)"
    cache.save_lesson(day, content, topic_override=topic_name)
    print(f"✅ Saved Quiz content (Topic: {topic_name})")
    
    # 2. Generate Reminder
    print("Generating Reminder...")
    rem_topic = "Quiz Review & Rest"
    rem_content = gemini.generate_reminder(day, topic_name=rem_topic)
    
     # Fix Header if needed
    if f"Day {day}" not in rem_content:
        rem_content = f"<h3>🌙 Nightly Check-in: Day {day}</h3>\n" + rem_content
        
    cache.save_reminder(day, rem_content)
    print("✅ Saved Reminder content.")
    
    print("\n✨ Day 6 Completed.")

if __name__ == "__main__":
    generate_day_6()
