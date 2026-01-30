import streamlit as st
import random
import re
from backend.lesson_manager import LessonManager
from backend.db_supabase import SupabaseManager
import streamlit.components.v1 as components

def extract_snippets(day, content):
    """(Same logic) Extracts engaging nuggets from lesson HTML."""
    snippets = []
    # 1. Code
    code_blocks = re.findall(r'<pre.*?><code.*?>(.*?)</code></pre>', content, re.DOTALL)
    for code in code_blocks:
        clean = code.strip()
        if len(clean) > 20:
            snippets.append({"type": "code", "day": day, "content": clean, "title": f"Snippet Day {day}"})
    # 2. Challenge
    match = re.search(r'<h3.*?>.*?Challenge.*?</h3>(.*?)<hr', content, re.DOTALL)
    if match:
        txt = re.sub(r'<[^>]+>', '', match.group(1)).strip() # unescape needed?
        if len(txt) > 50:
            snippets.append({"type": "challenge", "day": day, "content": txt, "title": f"Challenge Day {day}"})
    # 3. Headers
    headers = re.findall(r'<h3.*?>(.*?)</h3>', content)
    for h in headers:
        clean_h = re.sub(r'<[^>]+>', '', h).strip()
        if "Challenge" not in clean_h and len(clean_h) > 10:
             snippets.append({"type": "concept", "day": day, "content": clean_h, "title": f"Concept Day {day}"})
    return snippets

def get_random_feed_items(current_day, count=10):
    """Fetches random snippets from UNLOCKED lessons."""
    db = SupabaseManager()
    items = []
    
    # 1. Try High-Quality "Nuggets" (AI Refined)
    # ---------------------------------------------
    max_day = max(1, current_day)
    try:
        hq_nuggets = db.get_feed_nuggets(max_day, limit=count)
        if hq_nuggets:
            # Map DB fields to Feed fields if necessary (schema matches mostly)
            for n in hq_nuggets:
                items.append({
                    "day": n['lesson_day'],
                    "type": n['type'],
                    "title": n['title'],
                    "content": n['content'],
                    "source": "DB" # Explicit Source
                })
    except:
        pass # Fallback safely
        
    # 2. Fill gaps with "Regex Scraping" (Legacy/Fallback)
    # ----------------------------------------------------
    if len(items) < count:
        needed = count - len(items)
        available_days = list(range(1, max_day + 1))
        
        attempts = 0
        while len(items) < count and attempts < 30:
            day = random.choice(available_days)
            content = db.get_daily_content(day)
            attempts += 1
            if content:
                if snips:
                    chosen = random.choice(snips)
                    chosen['source'] = 'Scraper' # Explicit Source
                    items.append(chosen)
                    
    return items[:count]

def generate_feed_html(items):
    """Generates the Reel-style HTML with Scroll Snap."""
    
    cards_html = ""
    for item in items:
        # Determine Icon & Color
        if item['type'] == 'code':
            icon = "💻"
            badge_color = "#3b82f6"
            # Escape HTML for code block
            safe_content = item['content'].replace("<", "&lt;").replace(">", "&gt;")
            body = f'<pre><code class="language-python">{safe_content}</code></pre>'
        elif item['type'] == 'challenge':
            icon = "🔥"
            badge_color = "#ef4444"
            body = f'<div class="text-card">{item["content"]}</div>'
        else:
            icon = "💡"
            badge_color = "#a855f7"
            body = f'<div class="text-card concept">{item["content"]}</div>'
            
        cards_html += f"""
        <div class="reel-item">
            <div class="card-content">
                <div class="badge" style="background: {badge_color}20; color: {badge_color}; border: 1px solid {badge_color};">
                    {icon} <span>Day {item['day']}</span> • <span style="opacity:0.6; font-size:0.7em;">{item.get('source', 'DB')}</span>
                </div>
                <h3 style="color: {badge_color}">{item['title']}</h3>
                {body}
            </div>
            <div class="actions">
                <div class="action-btn">❤️</div>
                <div class="action-btn">🔖</div>
                <div class="action-btn">↗️</div>
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
                background: #0f172a; /* Dark Background */
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
                padding: 20px;
                border-bottom: 1px solid #1e293b;
                position: relative;
            }}
            
            .card-content {{
                background: #1e293b;
                border-radius: 20px;
                padding: 24px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
                border: 1px solid #334155;
            }}
            
            .badge {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            h3 {{ margin: 0 0 15px 0; font-size: 1.2rem; }}
            
            /* Text Logic */
            .text-card {{ font-size: 1.1rem; line-height: 1.6; color: #e2e8f0; }}
            .concept {{ font-weight: 600; font-size: 1.3rem; text-align: center; color: white; }}
            
            /* Code Logic */
            pre {{ margin: 0; border-radius: 12px; overflow: hidden; }}
            code {{ font-family: monospace; font-size: 0.9rem; }}
            
            /* Actions (Floating Right) */
            .actions {{
                position: absolute;
                right: 20px;
                bottom: 120px;
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            
            .action-btn {{
                width: 50px;
                height: 50px;
                background: rgba(30, 41, 59, 0.8);
                backdrop-filter: blur(5px);
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 1.5rem;
                border: 1px solid #334155;
                cursor: pointer;
                transition: transform 0.2s;
            }}
            
            .action-btn:active {{ transform: scale(0.9); }}
            
        </style>
    </head>
    <body>
        <div class="feed-container">
            {cards_html}
            
            <!-- End Logic -->
            <div class="reel-item" style="align-items: center; text-align: center;">
                 <h2 style="color: #94a3b8;">Caught up! 🚀</h2>
                 <p style="color: #64748b;">Complete more lessons to unlock more nuggets.</p>
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
        st.session_state.feed_cache = get_random_feed_items(current_day, 12) # Load batch of 12
        
    # Render Full Iframe
    html_code = generate_feed_html(st.session_state.feed_cache)
    components.html(html_code, height=800, scrolling=False) # Scrolling handled inside HTML
    
    # Reload Button (Outside Iframe)
    if st.button("🔄 Shuffle Feed", use_container_width=True):
        st.session_state.feed_cache = get_random_feed_items(current_day, 12)
        st.rerun()
