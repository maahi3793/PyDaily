import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'PyDaily')))

from backend.db_supabase import SupabaseManager
db = SupabaseManager()
contacts = db.admin_get_all_students()
emails = ['wkuldeepbpm@gmail.com', 'luckysri24@gmail.com', 'vedashrivilaseknathe@gmail.com', 'paragars1@gmail.com', 'myteliawork@gmail.com']
print("Checking users...")
for c in contacts:
    if c['email'] in emails:
        print(f"Email: {c['email']}, Day: {c.get('day')}, Status: {c.get('status')}")
