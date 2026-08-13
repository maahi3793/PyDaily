import os
import sys
import json
import logging
from dotenv import load_dotenv

# PAUSE ALL AUTOMATIONS
print("All automations are currently paused by Admin request.")
sys.exit(0)

# Ensure we are in the PyDaily directory or add to path
sys.path.append(os.getcwd())

# Force UTF-8 encoding for standard output to support emojis on Windows runners
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from backend import curriculum
from backend.db_supabase import SupabaseManager
from backend.gemini_service import GeminiService
from backend.lesson_manager import LessonManager

# Setup Logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pydaily.log"),
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)

def main():
    logging.info("Starting Scheduled Quiz Auto-Regeneration Script...")
    
    # Load Environment variables
    load_dotenv()
    
    # 1. Initialize Supabase and Gemini
    db = SupabaseManager()
    if not db.admin_supabase:
        logging.error("Supabase Admin Client not initialized. Check your environment variables.")
        sys.exit(1)
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Fallback to config loader
        from backend import config as config_loader
        config = config_loader.get_config()
        api_key = config.get('gemini_key')
        
    if not api_key:
        logging.error("Gemini API Key missing in environment.")
        sys.exit(1)
        
    gemini = GeminiService(api_key)
    cache = LessonManager()
    
    # 2. Identify all Quiz Days in the curriculum
    quiz_days = [day for day, topic in curriculum.TOPICS.items() if "Quiz" in topic or day % 3 == 0]
    # Filter to unique and sorted positive days
    quiz_days = sorted(list(set([int(d) for d in quiz_days if int(d) > 0])))
    
    logging.info(f"Checking {len(quiz_days)} quiz days defined in curriculum: {quiz_days}")
    
    # 3. Fetch all daily content to check existing quizzes
    # We fetch only the day and content fields to minimize memory/payload
    try:
        res = db.admin_supabase.table("daily_content").select("day, content").execute()
        existing_content = {row["day"]: row["content"] for row in res.data}
    except Exception as e:
        logging.error(f"Failed to query daily_content table: {e}")
        sys.exit(1)
        
    # 4. Find which quiz days need regeneration (unconditional if legacy/missing)
    legacy_or_missing_days = []
    
    for day in quiz_days:
        content = existing_content.get(day)
        if not content:
            # Skip future quiz days that have not been generated in the DB yet
            continue
            
        try:
            # Clean and parse JSON
            clean_json = content.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_json)
            questions = data.get("questions", [])
            
            # Check if any question lacks the new 'code_snippet' field (identifying it as legacy)
            is_legacy = False
            if not questions:
                is_legacy = True
            else:
                for q in questions:
                    # If 'code_snippet' is not a key in the question dict, it's legacy
                    if "code_snippet" not in q:
                        is_legacy = True
                        break
                        
            if is_legacy:
                legacy_or_missing_days.append((day, "Legacy JSON format (missing code_snippet field)"))
                
        except Exception as e:
            legacy_or_missing_days.append((day, f"Invalid JSON/Error: {e}"))
            
    logging.info(f"Found {len(legacy_or_missing_days)} quizzes that are legacy or missing.")
    
    if not legacy_or_missing_days:
        logging.info("All quizzes are up-to-date and conform to the new schema. Nothing to do!")
        return
        
    # 5. Process and regenerate up to 1 quizzes in this run
    max_regenerations = 1
    processed_count = 0
    
    for day, reason in legacy_or_missing_days:
        if processed_count >= max_regenerations:
            logging.info(f"Reached limit of {max_regenerations} regenerations per run. Exiting.")
            break
            
        logging.info(f"Regenerating Quiz for Day {day}. Reason: {reason}")
        
        # Determine strict 2-day scope (preceding two days)
        recent_days = [day - 2, day - 1]
        recent_topics = []
        for d in recent_days:
            if d > 0:
                topic_name = curriculum.TOPICS.get(d, f"Day {d} Concept")
                recent_topics.append(f"Day {d}: {topic_name}")
                
        logging.info(f"Scope for Day {day}: {recent_topics}")
        
        try:
            # Generate new quiz JSON using Gemini Service with Structured Outputs
            new_quiz_json = gemini.generate_quiz(day, recent_topics)
            
            # Save/Overwrite to DB
            cache.save_lesson(day, new_quiz_json, topic_override="Quiz Day (Review)")
            logging.info(f"Successfully regenerated and saved quiz for Day {day}.")
            processed_count += 1
            
        except Exception as e:
            error_msg = str(e).lower()
            logging.error(f"Failed to regenerate quiz for Day {day}: {e}")
            if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                logging.critical("API Quota Exhausted! Aborting the script entirely to prevent spamming the API.")
                import sys
                sys.exit(1)
            # Continue to next day
            continue
            
    logging.info(f"Finished run. Regenerated {processed_count} quizzes.")

if __name__ == "__main__":
    main()
