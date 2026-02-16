import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager
from tools.generate_nuggets_v2 import run_v2
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🔥 WIPING FEED TABLES...")
    db = SupabaseManager()
    
    if not db.admin_supabase:
        print("❌ Admin Key required for Wipe.")
        return

    try:
        # Delete all where id is not 0 (effectively all provided IDs are > 0)
        # Assuming id is integer. If uuid, use neq id, '0000...'? 
        # Safest: neq 'id', -1
        db.admin_supabase.table("feed_nuggets").delete().neq("id", -1).execute()
        print("✅ Table Wiped.")
    except Exception as e:
        print(f"❌ Wipe Failed: {e}")
        return
    
    print("🌱 Re-Seeding Days 1-22...")
    run_v2(1, 22)
    
if __name__ == "__main__":
    main()
