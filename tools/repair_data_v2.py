import os
import sys
import json
import logging

# Add project root to path ensures we can import backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from backend import curriculum
except ImportError:
    # Fallback to direct import if running from root
    import backend.curriculum as curriculum

# Setup List of files
HEADER = "\033[95m[IRONCLAD]\033[0m"

def repair():
    print(f"{HEADER} Starting Data Audit & Repair...")
    
    lessons_dir = "lessons"
    if not os.path.exists(lessons_dir):
        print(f"{HEADER} Error: 'lessons' directory not found at {os.getcwd()}")
        return

    # 1. PURGE BAD FILES
    print(f"{HEADER} scanning for corrupted files (Errors/Small)...")
    bad_files = 0
    
    files = os.listdir(lessons_dir)
    for f in files:
        if not f.endswith(".html"): continue
        path = os.path.join(lessons_dir, f)
        
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            reason = None
            if "Quota exceeded" in content: reason = "Quota Exceeded API Error"
            elif "429" in content and "error" in content.lower(): reason = "429 API Error"
            elif len(content) < 200: reason = "File too small (<200 bytes)"
            
            if reason:
                print(f"   🗑️ Deleting {f} -> Reason: {reason}")
                os.remove(path)
                bad_files += 1
        except Exception as e:
            print(f"   ⚠️ Error reading {f}: {e}")

    if bad_files == 0:
        print(f"{HEADER} No corrupted files found.")
    else:
        print(f"{HEADER} Purge Complete. Deleted {bad_files} files.")

    # 2. REBUILD MEMORY (topics.json)
    print(f"{HEADER} Rebuilding topics.json from Master Curriculum...")
    topics_path = os.path.join(lessons_dir, "topics.json")
    
    # Convert curriculum map (Int -> Str) to JSON friendly (Str -> Str)
    # We only care about ensuring the content matches curriculum.py
    new_memory = {str(k): v for k, v in curriculum.TOPICS.items()}
    
    with open(topics_path, 'w', encoding='utf-8') as f:
        json.dump(new_memory, f, indent=2)
        
    print(f"{HEADER} Memory Repaired. Mapped {len(new_memory)} topics from Curriculum.")
    print(f"{HEADER} OPERATION SUCCESSFUL.")

if __name__ == "__main__":
    repair()
