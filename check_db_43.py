import sys
import os

sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend.db_supabase import SupabaseManager

db = SupabaseManager()

print("Fetching Day 43 Reminder Content from DB...")
content = db.get_daily_reminder(43)
print("=== CONTENT ===")
print(repr(content))

print("\nFetching Day 43 Lesson Content from DB...")
lesson = db.get_daily_content(43)
if lesson:
    print(f"Lesson exists, length: {len(lesson)}")
else:
    print("Lesson is None!")
