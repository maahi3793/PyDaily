import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

def list_users():
    print("🕵️ listing All Users in Database...")
    db = SupabaseManager()
    
    if not db.admin_supabase:
        print("❌ Error: Service Key Missing.")
        return

    try:
        # 1. Fetch Auth Users
        users = db.admin_supabase.auth.admin.list_users()
        
        print(f"\n--- AUTH USERS ({len(users)}) ---")
        for u in users:
            # Filter for specific user if needed (optional)
            # if 'paragars' in u.email:
            if True:
                print(f"TARGET FOUND: {u.email}")
                try:
                    prof = db.admin_supabase.table('profiles').select('role, student_data(current_day, status)').eq('id', u.id).single().execute()
                    s_data = prof.data.get('student_data')
                    if isinstance(s_data, list) and s_data: s_data = s_data[0]
                    elif not isinstance(s_data, dict): s_data = {}
                    
                    day = s_data.get('current_day', 'N/A')
                    status = s_data.get('status', 'N/A')
                    print(f"   => ROLE: {prof.data.get('role')} | DAY: {day} | STATUS: {status}")
                    print(f"   => FULL DATA: {s_data}")
                except Exception as e:
                    print(f"   => ERROR: {e}")
                
    except Exception as e:
        print(f"❌ Failed to list users: {e}")

if __name__ == "__main__":
    list_users()
