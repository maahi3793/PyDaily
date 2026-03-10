import os
import logging
import re
from backend.db_supabase import SupabaseManager

class LessonManager:
    def __init__(self, lessons_dir="lessons"):
        self.lessons_dir = lessons_dir
        self.db = SupabaseManager() 
        
    def validate_content(self, content):
        """
        Gatekeeper: Prevents saving 'Quota Exceeded' or broken content.
        Returns (bool, message)
        """
        if not content: return False, "Empty Content"
        if len(content) < 100: return False, "Content too short (<100 chars)"
        
        # Check for Common API Errors (including Gemini error string prefixes)
        error_keywords = ["Quota exceeded", "429 Too Many Requests", "generate_content_free_tier_requests", "Error generating", "503 UNAVAILABLE"]
        for k in error_keywords:
            if k in content:
                return False, f"API Error Detected: {k}"
                
        return True, "Valid"

    def get_lesson(self, day):
        """Returns cached lesson content (DB Only)."""
        # DB Only
        content = self.db.get_daily_content(day)
        if content:
            logging.info(f"Cache Hit (DB): Loaded Day {day}.")
            return content
        return None

    def save_lesson(self, day, content, topic_override=None):
        """Saves generated lesson to DB ONLY (If Valid)."""
        # 1. Validation Logic
        is_valid, msg = self.validate_content(content)
        if not is_valid:
            logging.error(f"⛔ Content Validation Failed for Day {day}: {msg}")
            raise ValueError(f"Content Validation Failed: {msg}")

        # 2. Extract Topic
        if topic_override:
            topic = topic_override
        else:
            topic = self._extract_topic(content)
        
        # 3. Save to DB
        self.db.save_daily_content(day, content, topic)
        logging.info(f"✅ DB Saved: Day {day} Lesson.")

    def _extract_topic(self, content):
        match = re.search(r"<!--\s*TOPIC:\s*(.*?)\s*-->", content, re.IGNORECASE)
        if match:
             return match.group(1).strip()
        return "General Python"



    def get_reminder(self, day):
        # DB Only
        content = self.db.get_daily_reminder(day)
        return content

    def save_reminder(self, day, content):
        # 1. Validate
        is_valid, msg = self.validate_content(content)
        if not is_valid:
            logging.error(f"⛔ Reminder Validation Failed for Day {day}: {msg}")
            raise ValueError(f"Reminder Validation Failed: {msg}")

        # 2. Save to DB
        self.db.save_daily_reminder(day, content)
        logging.info(f"✅ DB Saved: Day {day} Reminder.")

    def get_motivation(self, date_str):
        # DB Only
        content = self.db.get_daily_motivation(date_str)
        return content

    def save_motivation(self, date_str, content):
        # 1. Validate
        is_valid, msg = self.validate_content(content)
        if not is_valid:
            logging.error(f"⛔ Motivation Validation Failed: {msg}")
            # We might be lenient with motivation, but strict is safer
            raise ValueError(f"Motivation Validation Failed: {msg}")

        # 2. Save to DB
        self.db.save_daily_motivation(date_str, content)
        logging.info(f"✅ DB Saved: Motivation for {date_str}.")

    def extract_practice_items(self, day):
        """
        Parses lesson content to find 'Daily Challenge' and 'Cumulative Practice' items.
        Returns a list of dicts: [{'title': '...', 'instruction': '...'}]
        """
        content = self.get_lesson(day)
        if not content: return []
        
        items = []
        import re
        
        # Helper to clean HTML
        def clean_html(text):
            text = re.sub(r'<br\s*/?>', '\n', text)
            text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text)
            text = re.sub(r'<code>(.*?)</code>', r'`\1`', text)
            text = re.sub(r'<[^>]+>', '', text) # Remove other tags
            import html
            return html.unescape(text).strip()

        # 1. Daily Challenge
        # Look for "Daily Challenge" header
        dc_match = re.search(r'Daily Challenge(.*?)(<h3|$)', content, re.DOTALL | re.IGNORECASE)
        if dc_match:
            raw_dc = dc_match.group(1)
            # It usually contains <p>Instructions</p> and <ol><li>Steps</li></ol>
            # Let's just grab all list items if present, or paragraph text
            dc_instr = clean_html(raw_dc)
            if len(dc_instr) > 10:
                items.append({
                    "title": "🎯 Daily Challenge",
                    "instruction": dc_instr
                })

        # 2. Cumulative Practice
        # Look for "Cumulative Practice" and the following <ol>
        cp_match = re.search(r'Cumulative Practice.*?(<ol>.*?</ol>)', content, re.DOTALL | re.IGNORECASE)
        if cp_match:
            ol_block = cp_match.group(1)
            # Extract list items
            lis = re.findall(r'<li>(.*?)</li>', ol_block, re.DOTALL)
            for li in lis:
                # Check for Title: Description format (<strong>Title:</strong> Description)
                title_match = re.search(r'<strong>(.*?):?</strong>', li)
                if title_match:
                    title = clean_html(title_match.group(1))
                    instr = clean_html(li.replace(title_match.group(0), ''))
                else:
                    title = "Practice Problem"
                    instr = clean_html(li)
                
                items.append({
                    "title": f"🏋️ {title}",
                    "instruction": instr
                })
                
        # FALLBACK: If no text items found, try the old code block extractor
        if not items:
            code_blocks = self.extract_practice_code(day)
            for i, code in enumerate(code_blocks):
                items.append({
                    "title": f"Code Snippet {i+1}",
                    "instruction": "Review and analyze this code:",
                    "code": code
                })
                
        return items

    def extract_practice_code(self, day):
        """
        Parses the stored lesson content for Day X and extracts the Python Code Block.
        Returns a list of code snippets found.
        """
        content = self.get_lesson(day)
        if not content: return []
        
        import re
        snippets = []
        
        # Pattern 1: HTML <pre><code> (Most likely from Gemini HTML)
        # Matches <pre ...><code ...> CONTENT </code></pre>
        html_pattern = r'<pre[^>]*><code[^>]*>(.*?)</code></pre>'
        matches = re.finditer(html_pattern, content, re.DOTALL)
        for m in matches:
            code = m.group(1)
            # Unescape HTML entities if needed (e.g. &lt; to <)
            import html
            code = html.unescape(code)
            snippets.append(code.strip())
            
        # Pattern 2: Markdown Fences (Backups)
        if not snippets:
            md_pattern = r'```python(.*?)```'
            matches = re.finditer(md_pattern, content, re.DOTALL)
            for m in matches:
                snippets.append(m.group(1).strip())
                
        return snippets
