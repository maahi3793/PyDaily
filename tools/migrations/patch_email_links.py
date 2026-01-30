import os
import sys

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager

def patch_links():
    print("🚀 Starting Email Link Patch...")
    db = SupabaseManager()
    
    if not db.admin_supabase:
        print("❌ Admin Key missing.")
        return

    # 1. Fetch all rows with reminder_content
    # Note: We fetch all day/reminder_content.
    res = db.admin_supabase.table('daily_content').select('day, reminder_content').execute()
    
    if not res.data:
        print("No content found.")
        return

    count = 0
    for row in res.data:
        day = row['day']
        content = row.get('reminder_content')
        
        if not content:
            continue
            
        initial_len = len(content)
        
        # 2. Perform Replacements
        # Target: <a href="https://github.com/maahi3793/PyDaily" ...>I'm Ready for Day {day_number + 1} 🚀</a>
        
        # We need to be careful with regex, or just replace the URL and the text separately if possible.
        # But the text "I'm Ready for Day X" is dynamic.
        # "https://github.com/maahi3793/PyDaily" is static.
        
        updated_content = content.replace("https://github.com/maahi3793/PyDaily", "https://pydaily.streamlit.app")
        
        # Now try to replace the Button Text using Regex because of the dynamic Day X
        import re
        # Pattern: >I'm Ready for Day \d+ 🚀<
        updated_content = re.sub(r">I'm Ready for Day \d+ 🚀<", ">Go to Student Portal 🚀<", updated_content)
        
        # Also handle potential variations or just "I'm Ready for Day"
        
        if updated_content != content:
            print(f"🔹 Patching Day {day}...")
            # 3. Update DB
            db.admin_supabase.table('daily_content').update({'reminder_content': updated_content}).eq('day', day).execute()
            count += 1
        else:
            print(f"🔸 Day {day} already up to date or no match.")

    print(f"✅ Patch Complete. Updated {count} rows.")

if __name__ == "__main__":
    patch_links()
