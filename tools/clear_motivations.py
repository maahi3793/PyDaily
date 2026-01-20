import os
import sys
import logging

# Path Setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend import data_manager

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def clear_motivations():
    print("🧹 Cleaning Daily Motivations Table...")
    db = data_manager.db
    
    try:
        # Delete all rows where date_str is NOT 'dummy' (effectively all)
        res = db.admin_supabase.table('daily_motivations').delete().neq('date_str', 'dummy').execute()
        count = len(res.data) if res.data else 0
        print(f"✅ Deleted {count} motivation entries.")
    except Exception as e:
        print(f"❌ Failed to clear motivations: {e}")
        print("Note: If the table doesn't have an 'id' column, we might need another delete strategy.")

if __name__ == "__main__":
    clear_motivations()
