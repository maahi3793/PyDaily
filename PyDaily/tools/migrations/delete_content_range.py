import os
import sys
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

logging.basicConfig(level=logging.INFO, format='%(message)s')

def delete_range(start_day):
    print(f"🗑️ Deleting content from Day {start_day} onwards...")
    db = SupabaseManager()
    
    try:
        res = db.admin_supabase.table('daily_content').delete().gte('day', start_day).execute()
        count = len(res.data) if res.data else 0
        print(f"✅ Successfully deleted {count} rows (Day {start_day}+).")
    except Exception as e:
        print(f"❌ Delete Failed: {e}")

if __name__ == "__main__":
    delete_range(7)
