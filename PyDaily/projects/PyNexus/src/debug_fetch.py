from services.content_manager import ContentManager
import sys

def debug():
    try:
        cm = ContentManager()
        data = cm.get_timeline_data()
        day1 = data.get(1, {})
        
        with open("src/debug_output.txt", "w", encoding="utf-8") as f:
            f.write("DAY 1 THEORY CONTENT FULL:\n")
            chap = day1.get('chapter', {})
            theory = chap.get('content_part1_theory', '')
            f.write(theory)
            f.write("\n\nIS HTML? " + str(theory.strip().startswith("<")))
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
