import os
import sys

# Path Setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend import curriculum

def refactor():
    original_topics = list(curriculum.TOPICS.values())
    new_map = {}
    
    topic_idx = 0
    day = 1
    
    # We want to fit ALL original topics.
    # We stop when we run out of topics.
    
    while topic_idx < len(original_topics):
        if day % 3 == 0:
            # Insert Quiz
            new_map[day] = f"Quiz Day (Review of Days {day-2}-{day-1})"
        else:
            # Insert Topic
            new_map[day] = original_topics[topic_idx]
            topic_idx += 1
        
        day += 1
        
    with open("temp_curriculum.txt", "w") as f:
        f.write("TOPICS = {\n")
        
        for d, t in new_map.items():
            f.write(f"    {d}: \"{t}\",\n")
            
        f.write("}\n")
        f.write(f"# Total Days: {len(new_map)}\n")
        
    print("✅ Written to temp_curriculum.txt")

if __name__ == "__main__":
    refactor()
