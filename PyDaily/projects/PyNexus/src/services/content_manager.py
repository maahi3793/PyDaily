from services.auth import AuthService

# Curriculum Topics Fallback (first 30 days for now)
CURRICULUM_TOPICS = {
    1: "Installation, Setup, and Your First 'Hello World'",
    2: "Variables and Simple Data Types (Integers, Floats)",
    3: "Quiz Day (Review)",
    4: "Basic Arithmetic and Order of Operations",
    5: "Introduction to Strings (Creation and Concatenation)",
    6: "Quiz Day (Review)",
    7: "Essential String Methods (.upper(), .lower(), .strip())",
    8: "String Slicing and Indexing",
    9: "Quiz Day (Review)",
    10: "User Input and Type Conversion (int(), str())",
    11: "Booleans and Comparison Operators",
    12: "Quiz Day (Review)",
    13: "Logical Operators (and, or, not)",
    14: "Control Flow: The if, elif, and else statements",
    15: "Quiz Day (Review)",
    16: "Introduction to Lists (Creating and Indexing)",
    17: "List Methods (Append, Insert, Remove, Pop)",
    18: "Quiz Day (Review)",
    19: "The for Loop (Iterating over Lists)",
    20: "The range() function and Loops",
    21: "Quiz Day (Review)",
    22: "The while Loop and Infinite Loops",
    23: "Control Statements (break, continue, pass)",
    24: "Quiz Day (Review)",
    25: "Introduction to Dictionaries (Key-Value pairs)",
    26: "Dictionary Methods (.keys(), .values(), .items())",
    27: "Quiz Day (Review)",
    28: "Introduction to Tuples (Immutability)",
    29: "Introduction to Sets (Uniqueness)",
    30: "Quiz Day (Review)",
}

class ContentManager:
    def __init__(self):
        self.auth = AuthService()
        self.client = self.auth.client

    def get_timeline_data(self):
        """
        Fetches LIGHTWEIGHT metadata (Title, Day) for the sidebar.
        Avoids fetching heavy content columns to speed up load time.
        """
        print("DEBUG: ContentManager.get_timeline_data() (Lightweight) called")
        if not self.client: return {}

        timeline = {}

        # 1. Fetch Daily Content Metadata
        try:
            mails = self.client.table("daily_content").select("day, topic").execute()
            for mail in mails.data:
                day = mail.get('day')
                if day:
                    # Use curriculum fallback if no title
                    fallback_title = CURRICULUM_TOPICS.get(day, f"Day {day} Content")
                    if day not in timeline: timeline[day] = {'title': fallback_title}
                    
                    if 'topic' in mail and mail['topic']:
                         timeline[day]['title'] = mail['topic']
        except Exception as e:
            print(f"ERROR: Failed to fetch daily_content metadata: {e}")

        # 2. Fetch Textbook Chapters Metadata
        try:
            chapters = self.client.table("textbook_chapters").select("day, title").execute()
            for chap in chapters.data:
                day = chap.get('day')
                if day:
                    # Use curriculum fallback if not already set
                    fallback_title = CURRICULUM_TOPICS.get(day, f"Day {day} Content")
                    if day not in timeline: timeline[day] = {'title': fallback_title}
                    if 'title' in chap and chap['title']:
                        db_title = chap['title']
                        # Skip generic placeholders - prefer curriculum topics
                        is_generic = (
                            db_title == "General Python" or
                            (db_title.startswith('Day ') and ('Content' in db_title or 'Python' in db_title))
                        )
                        print(f"DEBUG: Day {day} - DB title: '{db_title}', is_generic: {is_generic}, fallback: '{fallback_title}'")
                        if not is_generic:
                            timeline[day]['title'] = db_title
                        else:
                            # Use curriculum fallback for generic titles
                            timeline[day]['title'] = fallback_title
        except Exception as e:
            print(f"ERROR: Failed to fetch textbook_chapters metadata: {e}")
        
        # 3. Mark Boss Battles
        try:
            battles = self.client.table("boss_battles").select("day").execute()
            for battle in battles.data:
                day = battle.get('day')
                if day:
                    fallback_title = CURRICULUM_TOPICS.get(day, f"Day {day} Content")
                    if day not in timeline: timeline[day] = {'title': fallback_title}
                    timeline[day]['has_battle'] = True
        except Exception as e:
             print(f"ERROR: Failed to fetch boss_battles metadata: {e}")

        # [FILTER REMOVED] - Returning ALL days found in DB.
        sorted_timeline = dict(sorted(timeline.items()))
        print(f"DEBUG: Metadata loaded for {len(sorted_timeline)} days.")
        return sorted_timeline

    def get_day_content(self, day):
        """
        Fetches HEAVY content for a specific day.
        """
        print(f"DEBUG: Fetching full content for Day {day}...")
        if not self.client: return {}
        
        content = {'day': day}
        
        # 1. Get Topic/Mail Content
        try:
            res = self.client.table("daily_content").select("*").eq("day", day).execute()
            if res.data:
                data = res.data[0]
                content['topic_content'] = data.get('content') or data.get('topic_content') or ''
        except Exception as e: print(f"Error fetching topic: {e}")

        # 2. Get Chapter Content
        try:
            # [FIX] Use 'day' column only
            res = self.client.table("textbook_chapters").select("*").eq("day", day).execute()
            if res.data:
                content['chapter'] = res.data[0]
        except Exception as e: print(f"Error fetching chapter: {e}")

        # 3. Get Battle Content
        try:
            # [FIX] Use 'day' column only
            res = self.client.table("boss_battles").select("*").eq("day", day).execute()
            if res.data:
                content['battle'] = res.data[0]
        except Exception as e: print(f"Error fetching battle: {e}")
        
        return content

    def get_image_urls(self, image_ids):
        """
        Fetches image URLs for a list of image_ids from 'textbook_images' table.
        Returns: dict {id: url}
        """
        if not self.client or not image_ids:
            return {}
        
        try:
            # Supabase 'in' filter requires tuple or list
            # Syntax: .in_("column", [list])
            response = self.client.table("textbook_images") \
                .select("id, selected_url") \
                .in_("id", image_ids) \
                .execute()
            
            mapping = {item['id']: item['selected_url'] for item in response.data}
            print(f"DEBUG: Fetched {len(mapping)} images for placeholders.")
            return mapping
        except Exception as e:
            print(f"ERROR: Failed to fetch images: {e}")
            return {}
