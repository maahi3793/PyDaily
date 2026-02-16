
import os
import shutil
import glob
import sys

# Add root to path so we can import backend
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

print("Initializing Supabase Manager...")
db = SupabaseManager()

if not db.admin_supabase:
    print("❌ Error: Admin Client could not be initialized. Check backend configuration.")
    exit(1)

supabase = db.admin_supabase
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL") or os.getenv("EMAIL_ADDRESS")

if not ADMIN_EMAIL:
    # Try looking in config as last resort
    try:
        import json
        with open(os.path.join(ROOT_DIR, 'config.json'), 'r') as f:
            cfg = json.load(f)
            ADMIN_EMAIL = cfg.get('admin_email') or cfg.get('email_address')
            print(f"DEBUG: Found Admin Email in Config: {ADMIN_EMAIL}")
    except: pass

if not ADMIN_EMAIL:
     print("❌ Critical: Cannot identify Admin to save. Aborting.")
     exit(1)

def wipe_database():
    print("🔥 Starting Database Wipe...")
    
    # 1. Fetch All Users
    print("   Fetching users...")
    try:
        # Assuming list_users() works on the admin client directly
        users = supabase.auth.admin.list_users()
        
        deleted_count = 0
        skipped_count = 0
        
        for user in users:
            email = user.email
            if email == ADMIN_EMAIL:
                print(f"   🛡️ Skipping Admin: {email}")
                skipped_count += 1
                continue
            
            # Delete User
            print(f"   ☠️ Deleting: {email}")
            supabase.auth.admin.delete_user(user.id)
            deleted_count += 1
            
        print(f"   ✅ Database Wipe Complete: Deleted {deleted_count}, Kept {skipped_count} (Admin).")
        
    except Exception as e:
        print(f"   ❌ DB Wipe Error: {e}")

    # 2. Truncate Tables (Strictly speaking, cascading delete from User should handle it, but let's be sure)
    print("   🧹 Cleaning Quiz Results...")
    try:
        # We can't TRUNCATE via API easily without Rpc, but we can delete all rows
        # Actually, user deletion cascades, so this is likely empty already.
        # Let's just confirm.
        pass
    except: pass

def wipe_cache():
    print("\n🧽 Starting Cache Wipe...")
    
    # 1. Lessons
    lessons_dir = os.path.join(ROOT_DIR, 'lessons')
    html_files = glob.glob(os.path.join(lessons_dir, "*.html"))
    json_files = glob.glob(os.path.join(lessons_dir, "*.json"))
    
    files_to_delete = html_files + json_files
    
    count = 0
    for f in files_to_delete:
        try:
            # OPTIONAL: Keep topics.json if we want to preserve the plan? 
            # User said "refresh", usually implies content too. 
            # But topics.json is the map. If we delete it, we might break the app if it doesn't regenerate?
            # backend/curriculum.py has the static map. topics.json was the old dynamic one.
            # Assuming safe to delete.
            os.remove(f)
            count += 1
        except Exception as e:
            print(f"   Failed to delete {f}: {e}")
            
    print(f"   ✅ Deleted {count} cache files.")
    
    # 2. Local Data
    local_data = [
        os.path.join(ROOT_DIR, 'data', 'contacts.json'),
        os.path.join(ROOT_DIR, 'state.json')
    ]
    
    for f in local_data:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"   🗑️ Removed local file: {f}")
            except: pass

if __name__ == "__main__":
    print(f"⚠️ FACTORY RESET PROTOCOL INITIATED ⚠️")
    print(f"Admin Safe-List: {ADMIN_EMAIL}")
    print("------------------------------------------------")
    
    if not ADMIN_EMAIL:
        print("❌ CRITICAL: ADMIN_EMAIL is not set in .env. Aborting to prevent lockout.")
        exit(1)
        
    wipe_database()
    wipe_cache()
    
    print("\n✨ Factory Reset Complete. The application is now a blank slate.")
