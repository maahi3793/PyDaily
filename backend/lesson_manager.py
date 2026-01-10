import os
import logging
import re
import json

from backend.db_supabase import SupabaseManager

class LessonManager:
    def __init__(self, lessons_dir="lessons"):
        self.lessons_dir = lessons_dir
        self.topics_file = os.path.join(lessons_dir, "topics.json")
        self.db = SupabaseManager() # Hybrid Cache
        
        if not os.path.exists(lessons_dir):
            os.makedirs(lessons_dir)
            
        # Ensure topics file exists
        if not os.path.exists(self.topics_file):
            with open(self.topics_file, "w") as f:
                json.dump({}, f)

    def _get_path(self, day, type="lesson"):
        filename = f"day_{day}_{type}.html"
        return os.path.join(self.lessons_dir, filename)

    def get_lesson(self, day):
        """Returns cached lesson content (DB first, then File)."""
        # 1. Try DB (Persistent)
        content = self.db.get_daily_content(day)
        if content:
            logging.info(f"Cache Hit (DB): Loaded Day {day}.")
            return content
            
        # 2. Try File (Local/Fallback)
        path = self._get_path(day, "lesson")
        if os.path.exists(path):
            logging.info(f"Cache Hit (File): Loading Day {day}.")
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def save_lesson(self, day, content, topic_override=None):
        """Saves generated lesson to DB AND File."""
        # 1. Extract Topic (or use override)
        if topic_override:
            topic = topic_override
        else:
            topic = self._extract_topic(content)
        
        # 2. Save to DB (Primary)
        self.db.save_daily_content(day, content, topic)
        
        # 3. Save HTML File (Backup)
        path = self._get_path(day, "lesson")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Cache Saved: Day {day} Lesson.")
        
        # 4. Update Local Topics JSON (Legacy Support)
        self._update_local_topics(day, topic)

    def _extract_topic(self, content):
        match = re.search(r"<!--\s*TOPIC:\s*(.*?)\s*-->", content, re.IGNORECASE)
        if match:
             return match.group(1).strip()
        return "General Python"

    def _update_local_topics(self, day, topic):
        """Updates topics.json"""
        try:
            with open(self.topics_file, "r") as f:
                data = json.load(f)
        except:
            data = {}
            
        data[str(day)] = topic
        
        with open(self.topics_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_topics_history(self, up_to_day):
        """Returns list of topics up to specific day."""
        try:
            with open(self.topics_file, "r") as f:
                data = json.load(f)
            
            topics = []
            for d, t in data.items():
                if int(d) <= int(up_to_day):
                    topics.append(f"Day {d}: {t}")
            return "; ".join(topics)
        except Exception as e:
            logging.error(f"Error reading history: {e}")
            return "Basic Python Concepts"

    def get_reminder(self, day):
        # 1. Try DB
        content = self.db.get_daily_reminder(day)
        if content: return content
        
        # 2. Try File
        path = self._get_path(day, "reminder")
        if os.path.exists(path):
            logging.info(f"Cache Hit: Loading Day {day} Reminder from file.")
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def save_reminder(self, day, content):
        # 1. Save to DB
        self.db.save_daily_reminder(day, content)
        
        # 2. Save to File
        path = self._get_path(day, "reminder")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Cache Saved: Day {day} Reminder.")

    def get_motivation(self, date_str):
        """Returns cached motivation for a specific date (YYYY-MM-DD)."""
        # 1. Try DB
        content = self.db.get_daily_motivation(date_str)
        if content: return content
        
        # 2. Try File
        filename = f"motivation_{date_str}.html"
        path = os.path.join(self.lessons_dir, filename)
        if os.path.exists(path):
            logging.info(f"Cache Hit: Loading Motivation for {date_str}.")
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def save_motivation(self, date_str, content):
        # 1. Save to DB
        self.db.save_daily_motivation(date_str, content)
        
        # 2. Save to File
        filename = f"motivation_{date_str}.html"
        path = os.path.join(self.lessons_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Cache Saved: Motivation for {date_str}.")
