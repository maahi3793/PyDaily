"""
Welcome Tour Component
Interactive onboarding guide for first-time users.
"""
import streamlit as st

TOUR_STEPS = [
    {
        "title": "Welcome to PyDaily! 🎉",
        "content": """
        You've just joined a **180-day Python learning journey**!
        
        Let me show you around the portal so you can make the most of it.
        """,
        "icon": "👋"
    },
    {
        "title": "📚 Knowledge Vault",
        "content": """
        This is your **lesson library**. Every day, a new lesson appears here.
        
        - Read lessons at your own pace
        - Go back to review older topics
        - Lessons are saved forever - no expiry!
        """,
        "icon": "📖"
    },
    {
        "title": "🧠 Quiz Arena",
        "content": """
        Every **3rd day** is a Quiz Day!
        
        - Test what you've learned
        - Get instant feedback
        - Track your scores over time
        
        Pro tip: You can retake quizzes to improve your score!
        """,
        "icon": "🎯"
    },
    {
        "title": "💻 Practice Zone",
        "content": """
        Learning by doing is key! Here you'll find:
        
        - **Flashcards** - Quick concept review
        - **Boss Battles** - Challenging coding problems
        
        These unlock as you progress through the curriculum.
        """,
        "icon": "⚔️"
    },
    {
        "title": "📊 Progress Tracker",
        "content": """
        See how far you've come!
        
        - View your **learning roadmap**
        - Track quiz performance
        - Watch your skills grow
        """,
        "icon": "📈"
    },
    {
        "title": "📧 Daily Emails",
        "content": """
        You'll receive lessons via email based on your schedule:
        
        - **Morning** - Today's lesson
        - **Mid-day** - Motivation boost
        - **Evening** - Quiz reminders
        
        You can manage these in your profile settings.
        """,
        "icon": "✉️"
    },
    {
        "title": "You're All Set! 🚀",
        "content": """
        That's everything you need to know to get started!
        
        **Your first lesson arrives soon.** In the meantime:
        1. Download the **Starter Kit** to set up Python
        2. Explore the **Curriculum Roadmap** to see what's ahead
        
        Happy coding! 🐍
        """,
        "icon": "🎓"
    }
]


def render_welcome_tour():
    """
    Renders the welcome tour as a step-by-step modal experience.
    Uses session state to track progress through the tour.
    """
    # Initialize tour state
    if "tour_step" not in st.session_state:
        st.session_state.tour_step = 0
    if "tour_completed" not in st.session_state:
        st.session_state.tour_completed = False
    
    # If tour already completed, don't show
    if st.session_state.tour_completed:
        return False
    
    current_step = st.session_state.tour_step
    step = TOUR_STEPS[current_step]
    total_steps = len(TOUR_STEPS)
    
    # Tour Container Styles
    st.markdown("""
    <style>
    .tour-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #3b82f6;
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
    }
    .tour-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }
    .tour-icon {
        font-size: 2.5rem;
        background: rgba(59, 130, 246, 0.2);
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
    }
    .tour-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .tour-content {
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.8;
        margin-bottom: 25px;
    }
    .tour-progress {
        display: flex;
        gap: 8px;
        justify-content: center;
        margin-bottom: 20px;
    }
    .tour-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #334155;
    }
    .tour-dot.active {
        background: #3b82f6;
        width: 30px;
        border-radius: 5px;
    }
    .tour-dot.completed {
        background: #10b981;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Progress dots
    dots_html = ""
    for i in range(total_steps):
        if i < current_step:
            dots_html += '<div class="tour-dot completed"></div>'
        elif i == current_step:
            dots_html += '<div class="tour-dot active"></div>'
        else:
            dots_html += '<div class="tour-dot"></div>'
    
    st.markdown(f"""
    <div class="tour-container">
        <div class="tour-progress">{dots_html}</div>
        <div class="tour-header">
            <div class="tour-icon">{step['icon']}</div>
            <div class="tour-title">{step['title']}</div>
        </div>
        <div class="tour-content">{step['content']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_step > 0:
            if st.button("← Back", use_container_width=True):
                st.session_state.tour_step -= 1
                st.rerun()
    
    with col3:
        if current_step < total_steps - 1:
            if st.button("Next →", use_container_width=True, type="primary"):
                st.session_state.tour_step += 1
                st.rerun()
        else:
            if st.button("✅ Start Learning!", use_container_width=True, type="primary"):
                st.session_state.tour_completed = True
                st.rerun()
    
    with col2:
        if st.button("Skip Tour", use_container_width=True):
            st.session_state.tour_completed = True
            st.rerun()
    
    return True  # Tour is active


def should_show_tour(profile: dict) -> bool:
    """
    Determines if the welcome tour should be shown.
    Shows only for brand new users (Day 1, no tour completion flag).
    """
    if st.session_state.get("tour_completed"):
        return False
    
    current_day = profile.get('current_day', 1)
    has_seen_tour = profile.get('has_seen_tour', False)
    
    return current_day == 1 and not has_seen_tour
