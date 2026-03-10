import sys
import os

sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend.db_supabase import SupabaseManager

db = SupabaseManager()

print("Fetching all students...")
contacts = db.admin_get_all_students()
sent_contacts = [c for c in contacts if c.get('status') == 'lesson_sent']

print(f"Found {len(sent_contacts)} students stuck at 'lesson_sent'.")

for c in sent_contacts:
    email = c['email']
    current_day = c.get('day', 1)
    new_day = current_day + 1
    
    print(f"Updating {email}: Day {current_day} -> {new_day}, Status -> pending")
    db.admin_update_student_progress(email, day=new_day, status='pending')

print("All stuck students have been advanced to pending!")
