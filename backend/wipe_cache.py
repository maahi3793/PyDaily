import os
import shutil

def wipe_cache():
    lessons_dir = os.path.join(os.getcwd(), 'lessons')
    print(f"🧹 Wiping Cache Directory: {lessons_dir}")
    
    if os.path.exists(lessons_dir):
        # Iterate and remove all files
        for filename in os.listdir(lessons_dir):
            file_path = os.path.join(lessons_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"   Deleted: {filename}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"   ❌ Failed {filename}: {e}")
                
        # Re-create empty topics.json
        with open(os.path.join(lessons_dir, 'topics.json'), 'w') as f:
            f.write("{}")
        print("   ✅ Created fresh topics.json")
    else:
        print("   Directory not found (Nothing to wipe).")
        
    print("✨ Cache Cleaned.")

if __name__ == "__main__":
    wipe_cache()
