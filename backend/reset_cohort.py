from backend.db_supabase import SupabaseManager
import time

def reset_all_students():
    print("🚨 STARTING COHORT RESET 🚨")
    db = SupabaseManager()
    
    students = db.admin_get_all_students()
    print(f"Found {len(students)} students.")
    
    for s in students:
        email = s['email']
        print(f"🔄 Resetting {s['name']} ({email})...")
        success, msg = db.admin_update_student_progress(email, day=1, status='pending')
        if success:
            print(f"✅ Reset Complete")
        else:
            print(f"❌ Failed: {msg}")
            
    print("✨ ALL DONE. COHORT RESET TO DAY 1.")

if __name__ == "__main__":
    reset_all_students()
