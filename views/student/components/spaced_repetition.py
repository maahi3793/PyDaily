"""
Spaced Repetition Component
Surfaces review prompts for topics that haven't been reviewed recently.
Based on the SM-2 algorithm principle: review items at increasing intervals.
"""
import streamlit as st
import random
from datetime import datetime, timedelta
from backend import curriculum

# Rotating tips for variety
LEARNING_TIPS = [
    "💡 **Spaced Repetition Tip**: Reviewing topics at increasing intervals helps move information from short-term to long-term memory. Even a quick 5-minute review can significantly boost retention!",
    "💡 **Memory Hack**: The forgetting curve shows we lose 50% of new info within a day. A quick review resets that curve and strengthens memory!",
    "💡 **Pro Tip**: Teach what you learn! Explaining concepts to others (or even to yourself) is one of the most effective ways to solidify your understanding.",
    "💡 **Active Recall**: Instead of re-reading, try to recall the topic from memory first. This strengthens neural pathways far more effectively!",
    "💡 **Interleaving**: Mix up your review topics rather than focusing on one at a time. This improves long-term retention and problem-solving!",
    "💡 **The 2-Minute Rule**: If a review takes less than 2 minutes, do it now. Small consistent efforts compound into massive knowledge gains!",
]


def get_review_candidates(current_day: int, viewed_days: list = None):
    """
    Returns a list of days that should be reviewed based on spaced repetition.
    
    Review schedule:
    - Days > 7 days old: Suggest review
    - Days > 14 days old: Urgent review
    - Days > 30 days old: Critical review
    
    Only non-quiz days are suggested for review.
    """
    if viewed_days is None:
        viewed_days = []
    
    candidates = []
    today = current_day
    
    for day in range(1, min(today, 180)):  # Cap at day 180
        # Skip quiz days (every 3rd day)
        if day % 3 == 0:
            continue
        
        days_ago = today - day
        
        # Determine urgency
        if days_ago >= 30:
            urgency = "critical"
            color = "#EF4444"  # Red
            icon = "🔴"
        elif days_ago >= 14:
            urgency = "urgent"
            color = "#F59E0B"  # Amber
            icon = "🟠"
        elif days_ago >= 7:
            urgency = "normal"
            color = "#3B82F6"  # Blue
            icon = "🔵"
        else:
            continue  # Too recent, no need to review
        
        # Get topic name
        topic = curriculum.TOPICS.get(day, f"Day {day} Topic")
        
        candidates.append({
            "day": day,
            "topic": topic,
            "days_ago": days_ago,
            "urgency": urgency,
            "color": color,
            "icon": icon
        })
    
    # Sort by urgency (critical first) then by days_ago
    urgency_order = {"critical": 0, "urgent": 1, "normal": 2}
    candidates.sort(key=lambda x: (urgency_order[x['urgency']], -x['days_ago']))
    
    return candidates[:10]  # Limit to top 10 suggestions


def render_spaced_repetition(current_day: int):
    """
    Renders the spaced repetition review zone.
    Shows suggested topics to review based on time since last seen.
    """
    st.markdown("### 🧠 Review Zone")
    st.caption("Reinforce your knowledge with spaced repetition!")
    
    candidates = get_review_candidates(current_day)
    
    if not candidates:
        st.success("🎉 **You're all caught up!** No topics need review right now.")
        st.info("Keep progressing - review suggestions will appear as you advance.")
        return
    
    # Summary stats
    critical_count = len([c for c in candidates if c['urgency'] == 'critical'])
    urgent_count = len([c for c in candidates if c['urgency'] == 'urgent'])
    normal_count = len([c for c in candidates if c['urgency'] == 'normal'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 Critical", critical_count, help="Topics > 30 days old")
    with col2:
        st.metric("🟠 Urgent", urgent_count, help="Topics 14-30 days old")
    with col3:
        st.metric("🔵 Normal", normal_count, help="Topics 7-14 days old")
    
    st.divider()
    
    # Render review cards
    st.markdown("#### 📚 Suggested Reviews")
    
    for item in candidates:
        with st.container():
            col_icon, col_content, col_action = st.columns([0.5, 4, 1.5])
            
            with col_icon:
                st.markdown(f"<div style='font-size: 1.5rem;'>{item['icon']}</div>", unsafe_allow_html=True)
            
            with col_content:
                st.markdown(f"""
                **Day {item['day']}: {item['topic']}**  
                <span style='color: {item['color']}; font-size: 0.85rem;'>
                    {item['days_ago']} days ago
                </span>
                """, unsafe_allow_html=True)
            
            with col_action:
                # Use a link button to provide direct action
                if st.button(f"📖 Review", key=f"review_{item['day']}", use_container_width=True):
                    st.session_state["jump_to_lesson"] = item['day']
                    st.toast(f"✅ Go to **📚 Knowledge Vault** tab - Day {item['day']} is selected!")
    
    # Quick tip
    st.divider()
    st.info("💡 **Tip**: After clicking Review, switch to the **📚 Knowledge Vault** tab to see the lesson!")
    
    # Learning tip (dynamic from pool)
    tip_index = current_day % len(LEARNING_TIPS)
    st.markdown(f"> {LEARNING_TIPS[tip_index]}")
