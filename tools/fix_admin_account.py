import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

def fix_admin(email):
    print(f"🔧 Fixing Admin Account: {email}")
    db = SupabaseManager()
    
    if not db.admin_supabase:
        print("❌ Error: Service Key Missing. Cannot manage users.")
        return

    # 1. Check existence
    print("   Checking if user exists...")
    user_id = db.admin_get_user_id(email)

    if user_id:
        print(f"   ✅ User found (ID: {user_id}). Treating as Recovery.")
        # Reset Password
        print("   resetting password to: AdminRecovery123!")
        db.admin_supabase.auth.admin.update_user_by_id(user_id, {"password": "AdminRecovery123!"})
    else:
        print("   ⚠️ User NOT found. Creating Fresh.")
        # Create
        res = db.admin_supabase.auth.admin.create_user({
            "email": email,
            "password": "AdminRecovery123!",
            "email_confirm": True,
            "user_metadata": { "full_name": "Admin" }
        })
        user_id = res.user.id
        print(f"   ✅ Created User (ID: {user_id})")

    # 2. Ensure Profile & Role
    print("   Ensuring 'admin' role in profiles...")
    # Upsert profile to ensure row exists and role is admin
    db.admin_supabase.table('profiles').upsert({
        "id": user_id,
        "email": email,
        "role": "admin",
        "full_name": "Admin"
    }).execute()

    # 3. Ensure Student Data (just in case they want to test dashboard)
    print("   Ensuring student_data row...")
    db.admin_supabase.table('student_data').upsert({
        "student_id": user_id,
        "current_day": 1,
        "status": "pending"
    }).execute()

    print("\n✅ FIXED! You can now Log In.")
    print(f"📧 Email: {email}")
    print(f"🔑 Password: AdminRecovery123!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('email', nargs='?', help="Email to fix")
    args = parser.parse_args()
    
    target_email = args.email or os.getenv("ADMIN_EMAIL") or os.getenv("EMAIL_ADDRESS")
    
    if not target_email:
        # Fallback to config.json
        try:
            import json
            with open(os.path.join(ROOT_DIR, 'config.json')) as f:
                target_email = json.load(f).get('admin_email')
        except: pass
        
    if not target_email:
        print("❌ Could not determine Admin Email.")
        sys.exit(1)
        
    fix_admin(target_email)
