import json
import os
import sys

# Add root to path so we can import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_supabase import SupabaseManager

def load_json_safe(path):
    print("DEBUG: VERSION 3 (Binary Mode)")
    try:
        print(f"   Reading {path} in binary mode (forcing clean decode)...")
        with open(path, 'rb') as f:
            raw_data = f.read()
            # Decode with ignore to strip bad bytes
            print(f"   Read {len(raw_data)} bytes.")
            text = raw_data.decode('utf-8', errors='ignore')
            return json.loads(text)
    except Exception as e:
        print(f"❌ Failed to parse JSON: {e}")
        return None

def migrate():
    print("🚀 Starting Migration: JSON -> Supabase...")
    
    contacts = load_json_safe('contacts.json')
    
    if not contacts:
        print("❌ FAILED to read 'contacts.json'. File format might be corrupted.")
        return

    print(f"📦 Found {len(contacts)} contacts.")
    
    # 2. Connect DB
    try:
        db = SupabaseManager()
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    # 3. Insert Loop
    success_count = 0
    for c in contacts:
        email = c.get('email')
        name = c.get('name')
        day = c.get('day', 1)
        role = c.get('role', 'student') # Default to student
        
        print(f"   Uploading {email}...")
        try:
            db.add_user(email, name, role, day)
            success_count += 1
            print("   ✅ Done.")
        except Exception as e:
            # Check for conflict (already exists)
            msg = str(e)
            if "23505" in msg or "duplicate" in msg.lower():
                print("   ⚠️ User exists (skipped).")
            else:
                print(f"   ❌ Error: {msg}")
            
    print(f"\n🎉 Migration Complete. Processed {success_count}/{len(contacts)} users.")

if __name__ == "__main__":
    migrate()
