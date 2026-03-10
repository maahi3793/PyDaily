import sys
import os

sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend.db_supabase import SupabaseManager

db = SupabaseManager()

lesson = db.get_daily_content(43)
print("=== LESSON 43 ===")
print(lesson)
