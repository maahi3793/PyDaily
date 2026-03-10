import sys
import os

sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend.db_supabase import SupabaseManager

db = SupabaseManager()

lesson = db.get_daily_content(43)
with open('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/lesson_43.txt', 'w', encoding='utf-8') as f:
    f.write(lesson)
