import os
import logging
import re
import json

class LessonManager:
    def __init__(self, lessons_dir="lessons"):
        self.lessons_dir = lessons_dir
        self.topics_file = os.path.join(lessons_dir, "topics.json")
        
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
        """Returns cached lesson content or None if not found."""
        path = self._get_path(day, "lesson")
        if os.path.exists(path):
            logging.info(f"Cache Hit: Loading Day {day} Lesson from file.")
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def save_lesson(self, day, content):
        """Saves generated lesson to cache AND extracts/saves topic."""
        # 1. Save HTML File
        path = self._get_path(day, "lesson")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Cache Saved: Day {day} Lesson.")
        
        # 2. Extract & Save Topic
        self._extract_and_update_topic(day, content)

    def _extract_and_update_topic(self, day, content):
        """Finds <!-- TOPIC: ... --> and updates topics.json"""
        match = re.search(r"<!--\s*TOPIC:\s*(.*?)\s*-->", content, re.IGNORECASE)
        topic = "General Python"
        if match:
            topic = match.group(1).strip()
            logging.info(f"Extracted Topic for Day {day}: {topic}")
        else:
            logging.warning(f"No TOPIC tag found for Day {day}. Using default.")
            
        # Update JSON
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
        path = self._get_path(day, "reminder")
        if os.path.exists(path):
            logging.info(f"Cache Hit: Loading Day {day} Reminder from file.")
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def save_reminder(self, day, content):
        path = self._get_path(day, "reminder")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Cache Saved: Day {day} Reminder.")

    def get_motivation(self, date_str):
        """Returns cached motivation for a specific date (YYYY-MM-DD)."""
        filename = f"motivation_{date_str}.html"
        path = os.path.join(self.lessons_dir, filename)
        if os.path.exists(path):
            logging.info(f"Cache Hit: Loading Motivation for {date_str}.")
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def save_motivation(self, date_str, content):
        filename = f"motivation_{date_str}.html"
        path = os.path.join(self.lessons_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Cache Saved: Motivation for {date_str}.")
