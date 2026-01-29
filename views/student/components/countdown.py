"""
Countdown Timer Component
Shows anticipation builder for new students waiting for their first lesson.
"""
import streamlit as st
from datetime import datetime, timedelta
import pytz

def render_countdown():
    """
    Renders a beautiful countdown timer for Day 1 students.
    Shows time until the next scheduled lesson email (7:00 AM IST).
    """
    
    # Calculate next lesson time (7:00 AM IST tomorrow if past today's window)
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    # Next lesson is at 7:00 AM IST
    today_7am = now.replace(hour=7, minute=0, second=0, microsecond=0)
    
    if now < today_7am:
        next_lesson = today_7am
    else:
        next_lesson = today_7am + timedelta(days=1)
    
    # Calculate difference
    diff = next_lesson - now
    hours, remainder = divmod(int(diff.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Render the countdown UI
    st.markdown("""
    <style>
    .countdown-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        color: white;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
    }
    .countdown-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 10px;
        opacity: 0.9;
    }
    .countdown-subtitle {
        font-size: 1rem;
        opacity: 0.8;
        margin-bottom: 30px;
    }
    .countdown-boxes {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .countdown-box {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px 30px;
        min-width: 100px;
    }
    .countdown-number {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
    }
    .countdown-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.8;
        margin-top: 8px;
    }
    .countdown-footer {
        margin-top: 30px;
        font-size: 0.9rem;
        opacity: 0.7;
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="countdown-container">
        <div class="countdown-title">⏳ Your Python Journey Begins Soon!</div>
        <div class="countdown-subtitle">Your first lesson arrives in...</div>
        
        <div class="countdown-boxes">
            <div class="countdown-box pulse">
                <div class="countdown-number">{hours:02d}</div>
                <div class="countdown-label">Hours</div>
            </div>
            <div class="countdown-box pulse" style="animation-delay: 0.3s;">
                <div class="countdown-number">{minutes:02d}</div>
                <div class="countdown-label">Minutes</div>
            </div>
            <div class="countdown-box pulse" style="animation-delay: 0.6s;">
                <div class="countdown-number">{seconds:02d}</div>
                <div class="countdown-label">Seconds</div>
            </div>
        </div>
        
        <div class="countdown-footer">
            📧 Delivered to your inbox at 7:00 AM IST
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh hint
    st.caption("🔄 Refresh the page to update the countdown!")


def should_show_countdown(current_day: int, has_lesson: bool) -> bool:
    """
    Determines if the countdown should be shown.
    Shows only for Day 1 students who haven't received their first lesson yet.
    """
    return current_day == 1 and not has_lesson
