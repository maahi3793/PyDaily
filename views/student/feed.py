import streamlit as st
import random
import re
from backend.lesson_manager import LessonManager
from backend import curriculum

def extract_snippets(day, html_content):
    """Extracts engaging nuggets from lesson HTML using Regex."""
    snippets = []
    
    # 1. Extract Code Blocks (The meat!)
    code_blocks = re.findall(r'<pre.*?><code.*?>(.*?)</code></pre>', html_content, re.DOTALL)
    for i, code in enumerate(code_blocks):
        clean_code = code.strip()
        if len(clean_code) > 20: # Ignore tiny snippets
            snippets.append({
                "type": "code",
                "day": day,
                "content": clean_code,
                "title": f"Snippet from Day {day}"
            })

    # 2. Extract "Daily Challenge" Sections
    challenge_match = re.search(r'<h3.*?>.*?Daily Challenge.*?</h3>(.*?)<hr', html_content, re.DOTALL)
    if challenge_match:
        challenge_text = re.sub(r'<[^>]+>', '', challenge_match.group(1)).strip() # Strip HTML tags
        challenge_text = re.sub(r'\s+', ' ', challenge_text) # Normalize whitespace
        if len(challenge_text) > 50:
            snippets.append({
                "type": "challenge",
                "day": day,
                "content": challenge_text,
                "title": f"🔥 Challenge: Day {day}"
            })
            
    # 3. Extract Headers (Tips/Concepts)
    headers = re.findall(r'<h3.*?>(.*?)</h3>', html_content)
    for h in headers:
        if "Challenge" not in h and "Examples" not in h:
            snippets.append({
                "type": "concept",
                "day": day,
                "content": re.sub(r'<[^>]+>', '', h).strip(),
                "title": f"💡 Concept: Day {day}"
            })
            
    return snippets

from backend.db_supabase import SupabaseManager

# ... (extract_snippets function remains the same) ...

def get_random_feed_items(current_day, count=5):
    """Fetches random snippets from UNLOCKED lessons via Supabase."""
    db = SupabaseManager()
    items = []
    
    # Restrict to unlocked days (1 to current_day)
    # Ensure we have at least Day 1
    max_day = max(1, current_day)
    available_days = list(range(1, max_day + 1))
    
    attempts = 0
    while len(items) < count and attempts < 20:
        day = random.choice(available_days)
        
        # FETCH FROM SUPABASE DIRECTLY
        content = db.get_daily_content(day)
        attempts += 1
        
        if content:
            day_snippets = extract_snippets(day, content)
            if day_snippets:
                items.append(random.choice(day_snippets))
                
    return items

# ... (render_feed_card function remains the same) ...

def run(current_day):
    st.subheader("⚡ Infinite Knowledge Feed")
    st.caption(f"Doom scroll your unlocked knowledge (Days 1-{current_day}).")
    
    # Initialize Feed
    if "feed_items" not in st.session_state:
        st.session_state.feed_items = get_random_feed_items(current_day, 5)
        
    # Render Items
    if not st.session_state.feed_items:
        st.info("No snippets found yet! Complete more lessons to populate your feed.")
        if st.button("Refresh Feed", key="refresh_feed_empty"):
             st.session_state.feed_items = get_random_feed_items(current_day, 5)
             st.rerun()
    else:
        for item in st.session_state.feed_items:
            render_feed_card(item)
        
    # Load More Button
    if st.button("Load More Nuggets ⏬", use_container_width=True):
        new_items = get_random_feed_items(current_day, 3)
        st.session_state.feed_items.extend(new_items)
        st.rerun()
