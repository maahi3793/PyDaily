import os
import sys
import logging

# Path Setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def perform_hard_reset():
    print("🚨 INITIATING HARD RESET PROTOCOL 🚨")
    print("-----------------------------------")
    
    db = SupabaseManager()
    
    # 1. Wipe Quiz Data
    print("\n💥 Wiping Quiz Tables...")
    try:
        db.admin_supabase.table('quiz_results').delete().neq('id', 0).execute() # Hack to delete all
        db.admin_supabase.table('quiz_attempts').delete().neq('id', 0).execute()
        print("   ✅ Quiz Data Cleared.")
    except Exception as e:
        print(f"   ❌ Quiz Wipe Failed (Check RLS/Permissions?): {e}")

    # 2. Reset Students (Try multiple tables/columns to be safe)
    print("\n⏪ Rewinding ALL Students to Day 2 (Pending)...")
    
    attempts = [
        ('students', {'day': 2, 'status': 'pending'}),
        ('student_data', {'current_day': 2, 'status': 'pending'}),
        ('profiles', {'current_day': 2, 'status': 'pending'})
    ]
    
    success = False
    for table, payload in attempts:
        try:
            print(f"   Trying table '{table}'...")
            res = db.admin_supabase.table(table).update(payload).gt('id', '00000000-0000-0000-0000-000000000000').execute()
            if res.data:
                print(f"   ✅ Success! Reset {len(res.data)} rows in '{table}'.")
                success = True
            else:
                print(f"   ⚠️ Table '{table}' updated 0 rows (or empty).")
        except Exception as e:
            print(f"   ❌ Failed on '{table}': {e}")

    if not success:
        print("   ⚠️ WARNING: No rows were updated in any table. Check Table Names!")

    # 3. Wipe Content (Day 3+)
    print("\n🗑️  Deleting Generated Content (Day 3+)...")
    try:
        db.admin_supabase.table('daily_content').delete().gte('day', 3).execute()
        print("   ✅ Future Content (Day 3+) Deleted.")
    except Exception as e:
        print(f"   ❌ Content Wipe Failed: {e}")

    print("\n-----------------------------------")
    print("✨ Reset Complete. Ready for Monday Relaunch.")

if __name__ == "__main__":
    perform_hard_reset()
