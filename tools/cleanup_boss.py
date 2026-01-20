import os
import sys

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager

def cleanup_day(day):
    print(f"🗑️ Deleting Boss Battles for Day {day}...")
    db = SupabaseManager()
    
    if not db.admin_supabase:
        print("❌ Admin Key missing.")
        return

    # Delete
    res = db.admin_supabase.table('boss_battles').delete().eq('day', day).execute()
    print(f"✅ Deleted rows for Day {day}: {res}")

if __name__ == "__main__":
    cleanup_day(5)
