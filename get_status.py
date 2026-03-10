import sys
import os

sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend.db_supabase import SupabaseManager

db = SupabaseManager()
contacts = db.admin_get_all_students()
emails = ['wkuldeepbpm@gmail.com', 'luckysri24@gmail.com', 'vedashrivilaseknathe@gmail.com', 'paragars1@gmail.com', 'myteliawork@gmail.com']

with open('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/output_utf8.txt', 'w', encoding='utf-8') as f:
    for c in contacts:
        if c['email'] in emails:
            f.write(f"Email: {c['email']}, Day: {c.get('day')}, Status: {c.get('status')}\n")
