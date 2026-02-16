from services.content_manager import ContentManager

def debug():
    try:
        cm = ContentManager()
        data = cm.get_timeline_data()
        day1 = data.get(1, {})
        
        with open("src/mentor_debug.txt", "w", encoding="utf-8") as f:
            f.write("DAY 1 MENTOR CONTENT:\n")
            chap = day1.get('chapter', {})
            mentor = chap.get('content_part3_mentor', '')
            f.write(mentor)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
