import os
import sys

# Add root to path so we can import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager

def promote():
    print("👑 Promoting admin@pydaily.com...")
    
    try:
        db = SupabaseManager()
        
        # 1. Check Current Status
        # We use a raw select query to see what the ANON key sees (which might be nothing if RLS blocks it)
        # But wait, if RLS blocks Anon, we can't update it either!
        # CHECK: Do we have Service Role Key? NO. We only have ANON key.
        # This is the problem. Anon key cannot update other users' roles typically.
        
        # ACTUALLY: The only way to update this row via Python (without Service Key) is if RLS allows it.
        # RLS usually allows "Users to update their own data", but 'role' is usually protected.
        # If 'role' is protected, my Python script CANNOT update it.
        
        # HYPOTHESIS: RLS is blocking the UPDATE.
        
        print("   Attempting Update via Python (might fail if RLS protects 'role')...")
        res = db.supabase.table('users').update({'role': 'admin'}).eq('email', 'admin@pydaily.com').execute()
        
        if res.data:
            print(f"   ✅ Update Returned Data: {res.data}")
            if res.data[0]['role'] == 'admin':
                print("   🎉 SUCCESS: Role is definitely Admin.")
            else:
                print(f"   ❌ FAILED: Role is still {res.data[0]['role']}")
        else:
            print("   ⚠️ Update Returned NO Data. This usually means RLS blocked the update.")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    promote()
