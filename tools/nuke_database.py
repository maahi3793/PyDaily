import os
import sys

# Add root to path so we can import backend
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

def nuke():
    print("☢️ INITIATING NUCLEAR DATA WIPE ☢️")
    print("This will delete ALL Users, Profiles, Quiz Results, and Student Data.")
    
    db = SupabaseManager()
    if not db.admin_supabase:
        print("❌ Error: Service Key Missing. Cannot wipe DB.")
        return

    # 1. List All Users
    print("   Fetching all users...")
    try:
        users = db.admin_supabase.auth.admin.list_users()
        print(f"   Found {len(users)} users to delete.")
        
        for u in users:
            print(f"   Deleting User: {u.email} ({u.id})")
            db.admin_supabase.auth.admin.delete_user(u.id)
            
        print("✅ All Auth Users Deleted.")
        
        # 2. Truncate Tables (Optional, usually cascading deletes handle this, but to be sure)
        # Supabase-py client doesn't have a simple 'truncate', but we can delete all rows if RLS allows or Service Key bypasses.
        # Actually deleting users usually clears linked rows if "ON DELETE CASCADE" is set. 
        # If not, we might leave orphan rows. 
        # Our SQL schemas usually use References.
        
        # For 'quiz_results', which references student_id (auth.users), it should cascade.
        # For 'student_data', references student_id, cascades.
        # For 'profiles', references id, cascades.
        
        print("✅ Database should be clean (via Cascade).")
        
    except Exception as e:
        print(f"❌ Wipe Failed: {e}")

if __name__ == "__main__":
    nuke()
