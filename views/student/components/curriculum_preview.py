"""
Curriculum Preview Component
Shows a beautiful roadmap of the learning journey with phases and topics.
"""
import streamlit as st
from backend import curriculum

def get_phase_data():
    """Returns structured phase information for display."""
    return [
        {
            "phase": 1,
            "name": "🌱 Foundations",
            "days": "1-30",
            "color": "#10B981",  # Emerald
            "icon": "🐣",
            "topics": ["Variables", "Data Types", "Operators", "Strings", "Lists", "Tuples", "Dictionaries", "Sets", "Control Flow", "Loops"]
        },
        {
            "phase": 2,
            "name": "🔧 Core Skills",
            "days": "31-68",
            "color": "#3B82F6",  # Blue
            "icon": "🔨",
            "topics": ["Functions", "Modules", "File I/O", "Error Handling", "List Comprehensions", "Lambda Functions", "Map/Filter/Reduce"]
        },
        {
            "phase": 3,
            "name": "🏗️ OOP Mastery",
            "days": "69-90",
            "color": "#8B5CF6",  # Purple
            "icon": "🎭",
            "topics": ["Classes", "Objects", "Inheritance", "Polymorphism", "Encapsulation", "Magic Methods", "Decorators"]
        },
        {
            "phase": 4,
            "name": "🧠 CS Fundamentals",
            "days": "91-135",
            "color": "#F59E0B",  # Amber
            "icon": "🎓",
            "topics": ["Big O Notation", "Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs", "Sorting", "Searching"]
        },
        {
            "phase": 5,
            "name": "⚡ Pythonic Mastery",
            "days": "136-158",
            "color": "#EC4899",  # Pink
            "icon": "🐍",
            "topics": ["Iterators", "Generators", "Context Managers", "Type Hints", "Async Basics", "Testing"]
        },
        {
            "phase": 6,
            "name": "🚀 Professional",
            "days": "159-185",
            "color": "#14B8A6",  # Teal
            "icon": "💼",
            "topics": ["Concurrency", "Design Patterns", "APIs", "Database Integration", "Deployment", "Best Practices"]
        },
    ]


def render_curriculum_preview(current_day: int = 1):
    """
    Renders a beautiful curriculum roadmap.
    Shows locked/unlocked phases based on current progress.
    """
    phases = get_phase_data()
    
    # Inject CSS once
    st.markdown("""
    <style>
    .roadmap-container {
        padding: 20px 0;
    }
    .phase-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, rgba(30,41,59,0.9) 100%);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        border: 2px solid var(--border-color);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .phase-card:hover {
        transform: translateX(8px);
        border-color: var(--accent-color);
    }
    .phase-card.locked {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border-color: #64748b !important;
    }
    .phase-card.current {
        border: 3px solid #3B82F6;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.4);
    }
    .phase-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .phase-icon {
        font-size: 2rem;
    }
    .phase-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .phase-card.locked .phase-name {
        color: #94a3b8;
    }
    .phase-days {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-left: auto;
    }
    .phase-topics {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
    }
    .topic-tag {
        background: rgba(255,255,255,0.15);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .phase-card.locked .topic-tag {
        background: #334155;
        color: #94a3b8;
        border-color: #475569;
    }
    .phase-status {
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 1.5rem;
    }
    .connector {
        width: 4px;
        height: 30px;
        background: linear-gradient(to bottom, #475569, #334155);
        margin-left: 40px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🗺️ Your Learning Journey")
    st.caption("Here's what you'll master over the next 6 months")
    
    st.markdown('<div class="roadmap-container">', unsafe_allow_html=True)
    
    for i, phase in enumerate(phases):
        # Determine phase status
        day_range = phase["days"].split("-")
        start_day = int(day_range[0])
        end_day = int(day_range[1])
        
        if current_day > end_day:
            status_icon = "✅"
            card_class = ""
        elif current_day >= start_day:
            status_icon = "📍"
            card_class = "current"
        else:
            status_icon = "🔒"
            card_class = "locked"
        
        # Build topic tags HTML separately to avoid f-string issues
        topics_html = ""
        for t in phase['topics'][:6]:
            topics_html += f'<span class="topic-tag">{t}</span>'
        
        if len(phase['topics']) > 6:
            extra = len(phase['topics']) - 6
            topics_html += f'<span class="topic-tag">+{extra} more</span>'
        
        # Build card HTML
        card_html = f'''
        <div class="phase-card {card_class}" style="--card-bg: {phase['color']}30; --border-color: {phase['color']}60; --accent-color: {phase['color']};">
            <div class="phase-status">{status_icon}</div>
            <div class="phase-header">
                <span class="phase-icon">{phase['icon']}</span>
                <span class="phase-name">{phase['name']}</span>
                <span class="phase-days">Days {phase['days']}</span>
            </div>
            <div class="phase-topics">{topics_html}</div>
        </div>
        '''
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Connector line (except after last)
        if i < len(phases) - 1:
            st.markdown('<div class="connector"></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
