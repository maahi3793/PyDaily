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
            print(f"ID: {u.id} | Email: {u.email} | Confirmed: {u.email_confirmed_at is not None}")
            
            # Check Profile Role
            try:
                prof = db.admin_supabase.table('profiles').select('role').eq('id', u.id).single().execute()
                role = prof.data.get('role') if prof.data else "None"
                print(f"   -> Role: {role}")
            except:
                print("   -> Role: [Error/Missing Profile]")
                
    except Exception as e:
        print(f"❌ Failed to list users: {e}")

if __name__ == "__main__":
    list_users()
