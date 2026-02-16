import os
import sys

# Add root to path so we can import backend
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

def promote_to_admin(email):
    print(f"👑 Promoting {email} to ADMIN...")
    
    db = SupabaseManager()
    if not db.admin_supabase:
        print("❌ Error: Service Key Missing. Cannot perform admin operations.")
        return

    # 1. Find User ID
    user_id = db.admin_get_user_id(email)
    if not user_id:
        print(f"❌ User not found: {email}")
        print("👉 Please Sign Up first in the App (New Account tab).")
        return

    # 2. Update Role in Profiles
    try:
        res = db.admin_supabase.table('profiles').update({'role': 'admin'}).eq('id', user_id).execute()
        print(f"✅ Success! {email} is now an Admin.")
        print("Result:", res.data)
    except Exception as e:
        print(f"❌ Failed to update role: {e}")

if __name__ == "__main__":
    # Get email from env or input
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('email', nargs='?', help="Email to promote")
    args = parser.parse_args()
    
    target_email = args.email or os.getenv("ADMIN_EMAIL") or os.getenv("EMAIL_ADDRESS")
    
    if not target_email:
        print("❌ Admin Email not found in .env and not provided.")
        sys.exit(1)
        
    promote_to_admin(target_email)
