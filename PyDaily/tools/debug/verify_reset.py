import os
import sys
import logging

# Path Setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.db_supabase import SupabaseManager

def verify():
    print("🔍 Verifying Student Status (Row Scan)...")
    db = SupabaseManager()
    
    try:
        # Fetch status/day columns for up to 100 students
        res = db.admin_supabase.table('students').select('day, status').limit(100).execute()
        students = res.data
        
        total = len(students)
        reset_count = 0
        
        for s in students:
            if s['day'] == 2 and s['status'] == 'pending':
                reset_count += 1
            else:
                # Can't print email if we don't fetch it
                print(f"⚠️ Non-Reset Student Found (Day: {s['day']}, Status: {s['status']})")
        
        print(f"Total Students Checked: {total}")
        print(f"Reset Students Found: {reset_count}")
        
        if total == reset_count and total > 0:
            print("✅ VERIFIED: All students are reset.")
        elif total == 0:
            print("⚠️ No students found in DB.")
        else:
            print(f"❌ MISMATCH: {total - reset_count} students are NOT reset.")
            
    except Exception as e:
        print(f"❌ Verification Failed: {e}")

if __name__ == "__main__":
    verify()
