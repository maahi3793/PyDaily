import streamlit as st
import random
import re
from backend.lesson_manager import LessonManager
from backend.db_supabase import SupabaseManager
import streamlit.components.v1 as components

def get_random_feed_items(current_day, count=10):
    """Fetches V2 RICH Nuggets from Supabase."""
    db = SupabaseManager()
    items = []
    
    # Only fetch from DB. No fallback.
    # Users want quality over quantity.
    max_day = max(1, current_day)
    print(f"DEBUG: Fetching feed for Max Day: {max_day}")
    try:
        # We reuse the same db method, but the table schema has changed.
        # The 'content' field now contains full HTML.
        hq_nuggets = db.get_feed_nuggets(max_day, limit=count)
        print(f"DEBUG: Found {len(hq_nuggets) if hq_nuggets else 0} nuggets.")
        
        seen_content = set()
        
        if hq_nuggets:
            for n in hq_nuggets:
                html_content = n.get('content')
                
                # Deduplicate: Skip if we've seen this exact HTML before
                if html_content in seen_content:
                    continue
                seen_content.add(html_content)
                
                items.append({
                    "day": n.get('lesson_day'),
                    "html": html_content, 
                    "type": n.get('type')
                })
                
                # Stop if we have enough
                if len(items) >= count:
                    break
    except Exception as e:
        print(f"Feed Error: {e}")
        st.error(f"DB Error: {e}")
        
    return items

def generate_feed_html(items):
    """Generates the Reel-style HTML with Scroll Snap."""
    
    cards_html = ""
    for item in items:
        # The HTML is already pre-baked in the DB
        # We just wrap it in the reel-item container for snapping
        inner_html = item['html']
        
        cards_html += f"""
        <div class="reel-item">
            {inner_html}
            
            <!-- Actions Overlay -->
             <div class="actions">
                <div class="action-btn">❤️</div>
                <div class="action-btn">🔖</div>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Highlight.js for Code Styling -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
            
            * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
            
            body {{
                margin: 0;
                padding: 0;
                background: #000; /* Deep Black for V2 */
                color: white;
                font-family: 'Outfit', sans-serif;
                height: 100vh;
                overflow: hidden;
            }}
            
            .feed-container {{
                height: 100vh;
                overflow-y: scroll;
                scroll-snap-type: y mandatory;
                scroll-behavior: smooth;
            }}
            
            /* Hide Scrollbar */
            .feed-container::-webkit-scrollbar {{ display: none; }}
            .feed-container {{ -ms-overflow-style: none; scrollbar-width: none; }}
            
            .reel-item {{
                height: 100vh;
                width: 100%;
                scroll-snap-align: start;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 0; 
                position: relative;
            }}
            
            /* Actions (Floating Right) */
            .actions {{
                position: absolute;
                right: 20px;
                bottom: 15vh;
                display: flex;
                flex-direction: column;
                gap: 20px;
                z-index: 10;
            }}
            
            .action-btn {{
                width: 50px;
                height: 50px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 1.5rem;
                border: 1px solid rgba(255,255,255,0.2);
                cursor: pointer;
                transition: transform 0.2s;
            }}
            
            .action-btn:active {{ transform: scale(0.9); }}
            
        </style>
    </head>
    <body>
        <div class="feed-container">
            {cards_html}
            
             <div class="reel-item" style="background: #111;">
                 <div style="text-align: center; padding: 40px;">
                    <h2 style="color: #444;">You're caught up!</h2>
                    <p style="color: #666;">Check back tomorrow.</p>
                 </div>
            </div>
        </div>
        
        <script>hljs.highlightAll();</script>
    </body>
    </html>
    """

def run(current_day):
    # Setup
    st.markdown("### ⚡ Knowledge Reels")
    st.info("💡 Swipe up for next nugget!") # Hint for Desktop users
    
    if "feed_cache" not in st.session_state:
        st.session_state.feed_cache = get_random_feed_items(current_day, 12)
    
    # Render Full Iframe
    if st.session_state.feed_cache:
        html_code = generate_feed_html(st.session_state.feed_cache)
        components.html(html_code, height=800, scrolling=False)
    else:
        st.info("You're all caught up! 🚀 Check back tomorrow for more knowledge.")
        
    # Reload Button (Outside Iframe)
    if st.button("🔄 Shuffle Feed", use_container_width=True):
        st.session_state.feed_cache = get_random_feed_items(current_day, 12)
        st.rerun()
