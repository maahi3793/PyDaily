import sys
import os

sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend.db_supabase import SupabaseManager

db = SupabaseManager()
contacts = db.admin_get_all_students()
emails_to_check = ['myteliawork@gmail.com', 'wkuldeepbpm@gmail.com', 'luckysri24@gmail.com', 'vedashrivilaseknathe@gmail.com', 'paragars1@gmail.com']

print("--- STUDENT STATUS ---")
for c in contacts:
    if c['email'] in emails_to_check:
        print(f"Email: {c['email']}, Day: {c.get('day')}, Status: {c.get('status')}")

