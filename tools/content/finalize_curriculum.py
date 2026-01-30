import os
import sys

# Path Setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend import curriculum as old_curriculum

def finalize():
    # 1. Build New Map
    original_topics = list(old_curriculum.TOPICS.values())
    new_map = {}
    topic_idx = 0
    day = 1
    
    while topic_idx < len(original_topics):
        if day % 3 == 0:
            new_map[day] = f"Quiz Day (Review)"
        else:
            new_map[day] = original_topics[topic_idx]
            topic_idx += 1
        day += 1

    # 2. Define New File Content
    content = f"""# PyDaily Curriculum Map (Refactored)

# Metadata for Phases (Goals) - Adjusted for inserted Quiz Days (~1.5x expansion)
PHASE_GOALS = {{
    1: "Getting comfortable with syntax and basic logic.",
    2: "Writing reusable code and handling data.",
    3: "Structuring code using Classes and Objects.",
    4: "Computer Science fundamentals necessary for interviews and optimization.",
    5: "Mastering the 'Pythonic' way and internal mechanics.",
    6: "Concurrency, Architecture, and Professional Practices."
}}

def get_phase_info(day):
    # Phase 1: Originally 20 topics -> ~30 days
    if 1 <= day <= 30: return 1, PHASE_GOALS[1]
    
    # Phase 2: Originally 25 topics -> ~38 days (Ends ~Day 68)
    if 31 <= day <= 68: return 2, PHASE_GOALS[2]
    
    # Phase 3: Originally 15 topics -> ~23 days (Ends ~Day 90)
    if 69 <= day <= 90: return 3, PHASE_GOALS[3]
    
    # Phase 4: Originally 30 topics -> ~45 days (Ends ~Day 135)
    if 91 <= day <= 135: return 4, PHASE_GOALS[4]
    
    # Phase 5: Originally 15 topics -> ~23 days (Ends ~Day 158)
    if 136 <= day <= 158: return 5, PHASE_GOALS[5]
    
    # Phase 6: Originally 15 topics -> ~23 days (Ends ~Day 181)
    if 159 <= day <= 185: return 6, PHASE_GOALS[6]
    
    return 1, PHASE_GOALS[1] # Default

# Topic Map (Auto-Generated with Quiz Intervals)
TOPICS = {{
"""
    # 3. Append Topics
    for d, t in new_map.items():
        content += f'    {d}: "{t}",\n'
    
    content += "}\n"

    # 4. Write to Target File
    target_path = os.path.join(ROOT_DIR, "backend", "curriculum.py")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ Successfully updated {target_path} with {len(new_map)} days.")

if __name__ == "__main__":
    finalize()
