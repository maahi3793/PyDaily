import os
import time
from backend import data_manager
from backend.db_supabase import SupabaseManager

def run_migration():
    print("🚀 Starting Migration: Excel -> Supabase")
    
    # 1. Connect to DB
    db = SupabaseManager()
    if not db.admin_supabase:
        print("❌ CRITICAL: SUPABASE_SERVICE_KEY missing in .env")
        print("Please add it and try again.")
        return

    # 2. Get Source Data (Excel/JSON)
    # data_manager.get_contacts() handles reading from the active source
    contacts = data_manager.get_contacts()
    
    if not contacts:
        print("⚠️ No contacts found in source.")
        return

    print(f"📦 Found {len(contacts)} students to migrate.")
    
    success_count = 0
    
    for student in contacts:
        email = student.get('email')
        name = student.get('name', 'Student')
        day = student.get('day', 1)
        status = student.get('status', 'pending')
        
        print(f"\nProcessing {email}...")
        
        # A. Try Creating User (If not exists)
        # Note: If password logic is strictly 'Invite', we'd do that.
        # Here we seed with a default password so Admin can share it or they can reset.
        created, msg = db.admin_create_student(email, name, "Welcome123!")
        
        if created:
            print(f"   ✅ Created User: {email}")
        else:
            if "already exists" in msg.lower() or "registered" in msg.lower():
                 print(f"   ℹ️ User exists. Syncing progress...")
            else:
                 print(f"   ❌ Creation Failed: {msg}")
                 
        # B. Sync Progress (Day/Status)
        # Even if user existed, we want Excel to be the Source of Truth for *Progress* right now.
        updated = db.admin_update_student_progress(email, day, status)
        if updated:
            print(f"   ✅ Progress Synced: Day {day} | {status}")
            success_count += 1
        else:
            print(f"   ❌ Progress Sync Failed")

    print(f"\n✨ Migration Complete: {success_count}/{len(contacts)} students synced.")
    print("\nNEXT STEP: Update data_manager.py to read from Supabase permanently.")

if __name__ == "__main__":
    run_migration()
