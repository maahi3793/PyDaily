import os
import logging

class LessonManager:
    def __init__(self, lessons_dir="lessons"):
        self.lessons_dir = lessons_dir
        if not os.path.exists(lessons_dir):
            os.makedirs(lessons_dir)

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
        """Saves generated lesson to cache."""
        path = self._get_path(day, "lesson")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Cache Saved: Day {day} Lesson.")

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
