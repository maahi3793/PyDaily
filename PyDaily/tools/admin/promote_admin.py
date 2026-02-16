import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

def promote(email):
    print(f"👑 Promoting {email} to ADMIN...")
    db = SupabaseManager()
    
    if not db.admin_supabase:
        print("❌ Error: Service Key Missing.")
        return

    user_id = db.admin_get_user_id(email)
    if not user_id:
        print(f"❌ User not found: {email}")
        return

    try:
        db.admin_supabase.table('profiles').update({'role': 'admin'}).eq('id', user_id).execute()
        print(f"✅ Success! {email} is now an Admin.")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('email', nargs='?', help="Email to promote")
    args = parser.parse_args()
    
    target_email = args.email or os.getenv("ADMIN_EMAIL") or os.getenv("EMAIL_ADDRESS")
    if not target_email:
        print("❌ No email provided.")
        sys.exit(1)
        
    promote(target_email)
