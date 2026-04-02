import os
import logging
from backend.db_supabase import SupabaseManager

logging.basicConfig(level=logging.INFO, format='%(message)s')

def fix_day_63():
    db = SupabaseManager()
    day = 63
    
    print(f"--- Emergency Repair: Day {day} ---")
    
    # 1. Delete corrupted content from daily_content
    # Note: daily_content PK is 'day'
    try:
        print(f"🧹 Removing corrupted 'Apology' content from daily_content for Day {day}...")
        res = db.admin_supabase.table('daily_content').delete().eq('day', day).execute()
        print(f"✅ Success: {res.data}")
    except Exception as e:
        print(f"❌ Failed to delete content: {e}")

    # 2. Reset students from 'lesson_sent' back to 'pending'
    # This ensures they get the REAL quiz tomorrow/now.
    try:
        print(f"🔄 Finding students stuck on Day {day} with 'lesson_sent' status...")
        # Get all students
        students = db.admin_get_all_students()
        affected = [s for s in students if s.get('day') == day and s.get('status') == 'lesson_sent']
        
        print(f"Found {len(affected)} students to reset.")
        
        for student in affected:
            email = student.get('email')
            print(f"  - Resetting {email}...")
            db.admin_update_student_progress(email, status='pending')
            
        print("✅ Student Reset Complete.")
    except Exception as e:
        print(f"❌ Failed to reset students: {e}")

if __name__ == "__main__":
    fix_day_63()
