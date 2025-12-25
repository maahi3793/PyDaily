import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.db_supabase import SupabaseManager

def seed():
    print("🌱 Seeding Supabase with initial Admin user...")
    db = SupabaseManager()
    
    # 1. Add Default Admin
    config = {
        "email": "admin@pydaily.com", 
        "name": "PyDaily Admin",
        "role": "admin",
        "day": 100
    }
    
    try:
        db.add_user(config['email'], config['name'], config['role'], config['day'])
        print(f"✅ Created User: {config['email']}")
    except Exception as e:
        print(f"⚠️ Could not create (maybe exists): {e}")

    # 2. Add Test Student
    student = {
        "email": "student@test.com",
        "name": "Test Student",
        "role": "student",
        "day": 3
    }
    try:
        db.add_user(student['email'], student['name'], student['role'], student['day'])
        print(f"✅ Created User: {student['email']}")
    except Exception as e:
        print(f"⚠️ Could not create student: {e}")

if __name__ == "__main__":
    seed()
