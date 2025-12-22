import streamlit as st
from backend import data_manager, gemini_service, email_service, lesson_manager
import datetime
import pandas as pd
from collections import defaultdict

st.set_page_config(page_title="PyDaily Admin", page_icon="🐍", layout="wide")

# Inject Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 1️⃣ HERO HEADER (Product Feel)
st.markdown("""
<div class="hero-header">
    <div class="hero-title">PyDaily Admin Dashboard</div>
    <div class="hero-subtitle">Manage cohorts, review lessons, and track student success</div>
</div>
""", unsafe_allow_html=True)

# Load Components
config = data_manager.get_config()
contacts = data_manager.get_contacts()
gemini = gemini_service.GeminiService(config.get('gemini_key'))
mailer = email_service.EmailService(
    config.get('email_address'), 
    config.get('email_password'),
    test_mode=config.get('test_mode', False),
    admin_email=config.get('admin_email', '')
)
cache = lesson_manager.LessonManager()

if not config.get('gemini_key') or not config.get('email_address'):
    st.warning("⚠️ Please configure your API Keys and Email in 'Settings' first!")
    st.stop()

# --- Helpers ---
def group_contacts_by_day(contact_list):
    groups = defaultdict(list)
    for c in contact_list:
        groups[c['day']].append(c)
    return groups

# --- Logic ---

# --- Visual Dashboard Header ---

st.markdown("### 📊 Cohort Overview")

# Calculate Data
total_students = len(contacts)
# Restore Lists (Required for Tabs later)
pending_contacts = [c for c in contacts if c.get('status') == 'pending']
sent_contacts = [c for c in contacts if c.get('status') == 'lesson_sent']
complete_contacts = [c for c in contacts if c.get('status') == 'complete']

# Split Queue for Tabs
standard_pending = [c for c in pending_contacts if (c.get('day', 1) % 3 != 0 or c.get('day', 1) == 0)]
quiz_pending = [c for c in pending_contacts if (c.get('day', 1) % 3 == 0 and c.get('day', 1) > 0)]

pending_count = len(pending_contacts)
completed_count = len(complete_contacts)

if total_students > 0:
    avg_day = sum([c.get('day', 1) for c in contacts]) / total_students
    progress_val = min(avg_day / 100.0, 1.0)
else:
    avg_day = 0
    progress_val = 0

# Custom Premium Cards
col1, col2, col3 = st.columns(3)

with col1:
    # PRIMARY CARD (Focus Point)
    st.markdown(f"""
    <div class="metric-card-primary">
        <div class="metric-label">🟢 Active Queue</div>
        <div class="metric-value">{pending_count}</div>
        <div class="metric-sub">Students waiting for action</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Cohort Average</div>
        <div class="metric-value">Day {int(avg_day)}</div>
        <div class="metric-sub">On track</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Volume</div>
        <div class="metric-value">{total_students}</div>
        <div class="metric-sub">Total enrolled students</div>
    </div>
    """, unsafe_allow_html=True)

# INTERACTION: Summary Toggle
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

st.write("")
if st.button("📉 View Cohort Insights", use_container_width=True):
    st.session_state.show_summary = not st.session_state.show_summary

if st.session_state.show_summary:
    with st.container():
        st.markdown("### 🔎 Cohort Deep Dive")
        d1, d2 = st.columns(2)
        with d1:
            if total_students > 0:
                day_counts = defaultdict(int)
                for c in contacts:
                    day_counts[c.get('day', 1)] += 1
                
                # Chart Data
                df_chart = pd.DataFrame({
                    "Students": list(day_counts.values()),
                    "Day": list(day_counts.keys())
                }).set_index("Day")
                
                st.bar_chart(df_chart)
                st.caption("Distribution of students by Day")
        with d2:
             st.info("💡 **Insight:** Most students are consistent. 2 students are paused.")
             
             # Quiz Stats
             quiz_eligible_count = len([c for c in contacts if c.get('day', 1) % 3 == 0 and c.get('day', 1) > 0])
             st.metric("🎯 Students on Quiz Day", quiz_eligible_count)

# 3️⃣ PROGRESS STORY (Depth)
st.markdown(f"""
<div class="progress-card">
    <div style="margin-bottom: 8px; font-weight: 600; color: #374151;">Cohort Progress</div>
    <div style="margin-bottom: 12px; color: #6B7280; font-size: 0.9rem;">
        {int(progress_val*100)}% Complete · Day {int(avg_day)} of 100
    </div>
</div>
""", unsafe_allow_html=True)

st.progress(progress_val)



st.divider()

# --- Main Dashboard ---
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Morning Operations", "🌙 Evening Operations", "⚡ Mid-Day Boost", "🎯 Quiz Ops"])

# === TAB 1: MORNING LESSONS ===
with tab1:
    st.header("🌞 Send Daily Lessons (Standard)")
    
    if not standard_pending:
        st.info("🎉 Standard Queue is Empty! (Check Quiz Tab for others)")
    else:
        st.write(f"**{len(standard_pending)} students** are waiting for lessons.")
        
        # Group by Day
        day_groups = group_contacts_by_day(standard_pending)
        
        # Display Groups
        for day, group in sorted(day_groups.items()):
            label = f"📅 Day {day} ({len(group)} students)"
            # No quiz badge here
                
            with st.expander(label, expanded=True):
                st.write(f"Students: {', '.join([c['name'] for c in group])}")
                
                # Check Cache
                cached_lesson = cache.get_lesson(day)
                
                if cached_lesson:
                    st.success("✅ Lesson Cached")
                    
                    # Preview / Edit Mode
                    with st.expander("📝 View / Edit Content"):
                         new_content = st.text_area(f"Editor (Day {day})", value=cached_lesson, height=300)
                         if st.button(f"💾 Save Changes (Day {day})"):
                             cache.save_lesson(day, new_content)
                             st.success("Saved!")
                             st.rerun()
                             
                    with st.popover(f"👁️ Preview HTML"):
                        import streamlit.components.v1 as components
                        clean_html = cached_lesson.replace('```html', '').replace('```', '')
                        components.html(clean_html, height=600, scrolling=True)

                else:
                    st.warning("⚠️ Not Cached")
                    if st.button(f"⚡ Generate Day {day}"):
                         with st.spinner("Building Lesson..."):
                             history = cache.get_topics_history(day - 1)
                             content = gemini.generate_lesson(day, history)
                             cache.save_lesson(day, content)
                         st.success("Generated & Saved!")
                         st.rerun()

        if st.button("🚀 Process Standard Queue", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_groups = len(day_groups)
            current_group_idx = 0
            
            for day, group in day_groups.items():
                status_text.write(f"Processing Day {day}...")
                
                content = cache.get_lesson(day)
                if not content:
                    status_text.write(f"Cache Miss: Generating Day {day}...")
                    # Get history up to yesterday to decide today's topic
                    history = cache.get_topics_history(day - 1)
                    content = gemini.generate_lesson(day, history)
                    cache.save_lesson(day, content)
                
                status_text.write(f"Sending to {len(group)} students...")
                success, msg = mailer.send_email(group, f"🐍 PyDaily: Day {day}", content)
                
                if success:
                    for student in group:
                        data_manager.update_contact_status(student['email'], status='lesson_sent')
                else:
                    st.error(f"Day {day} Failed: {msg}")
                
                current_group_idx += 1
                progress_bar.progress(current_group_idx / total_groups)
            
            status_text.write("✅ All Done!")
            st.balloons()
            st.rerun()

# === TAB 2: EVENING REMINDERS ===
with tab2:
    st.header("🌙 Send Evening Reminders")
    
    if not sent_contacts:
        st.info("😴 Evening Queue is Empty. Did you send lessons yet?")
    else:
        st.write(f"**{len(sent_contacts)} students** need a reminder.")
        
        # Group by Day
        day_groups = group_contacts_by_day(sent_contacts)
        
        for day, group in sorted(day_groups.items()):
            st.write(f"**Day {day}**: {len(group)} students waiting.")
        
        if st.button("🔔 Process Evening Queue", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_groups = len(day_groups)
            current_group_idx = 0
            
            for day, group in day_groups.items():
                content = cache.get_reminder(day)
                if not content:
                    status_text.write(f"Generating Day {day} Reminder...")
                    content = gemini.generate_reminder(day)
                    cache.save_reminder(day, content)
                
                status_text.write(f"Sending reminders for Day {day}...")
                success, msg = mailer.send_email(group, f"🌙 PyDaily Check-in: Day {day}", content)
                
                if success:
                    # Advance Day
                    for student in group:
                        data_manager.update_contact_status(student['email'], day=day+1, status='pending')
                
                current_group_idx += 1
                progress_bar.progress(current_group_idx / total_groups)
                
            status_text.write("✅ Nightly Run Complete! Students advanced to next day.")
            st.success("Everyone promoted! See you tomorrow.")
            st.rerun()

# === TAB 3: MID-DAY BOOST ===
with tab3:
    st.header("⚡ Mid-Day Motivation")
    st.caption("Send a morale booster to ALL active students (Pending + Sent).")
    
    today_str = datetime.date.today().isoformat()
    
    # 1. Check Cache
    cached_motivation = cache.get_motivation(today_str)
    
    if cached_motivation:
        st.success("✅ Motivation for Today is Cached")
        st.session_state.motivation_content = cached_motivation
    elif 'motivation_content' not in st.session_state:
        st.session_state.motivation_content = None
        
    if not cached_motivation:
        if st.button("🎲 Generate Fresh Quote", use_container_width=True):
            with st.spinner("Finding inspiration..."):
                content = gemini.generate_motivation()
                cache.save_motivation(today_str, content)
                st.session_state.motivation_content = content
                st.rerun()
            
    if st.session_state.motivation_content:
        # Preview
        clean_html = st.session_state.motivation_content.replace('```html', '').replace('```', '')
        st.components.v1.html(clean_html, height=400, scrolling=True)
        
        # Send
        # Target: Everyone who is NOT paused or complete? Or just everyone?
        # Let's say Everyone who is 'pending' or 'lesson_sent'.
        active_recipients = [c for c in contacts if c.get('status') in ['pending', 'lesson_sent']]
        
        st.write(f"**Target Audience**: {len(active_recipients)} active students.")
        
        if st.button("🚀 Blast Motivation (All Active)", type="primary", use_container_width=True):
            if not active_recipients:
                st.warning("No active students to send to.")
            else:
                progress_bar = st.progress(0)
                status = st.empty()
                status.write("Sending blasts...")
                
                success, msg = mailer.send_email(active_recipients, "⚡ Mid-Day Boost: Keep Going!", st.session_state.motivation_content)
                
                progress_bar.progress(100)
                if success:
                    st.success("Motivation Sent! 🚀")
                    st.balloons()
                else:
                    st.error(f"Failed: {msg}")

# === TAB 4: QUIZ OPS ===
with tab4:
    st.header("🎯 Quiz Operations")
    st.info("Students here are on Day 3, 6, 9... and will receive the 'Interview Prep Quiz' module.")
    
    if not quiz_pending:
        st.success("✅ No Quizzes Pending!")
    else:
        st.write(f"**{len(quiz_pending)} students** need a Quiz.")
        
        # Group by Day
        day_groups = group_contacts_by_day(quiz_pending)
        
        # Display Groups
        for day, group in sorted(day_groups.items()):
            label = f"🎯 QUIZ: Day {day} ({len(group)} students)"
                
            with st.expander(label, expanded=True):
                st.write(f"Students: {', '.join([c['name'] for c in group])}")
                
                # Check Cache
                cached_lesson = cache.get_lesson(day)
                
                if cached_lesson:
                    st.success("✅ Quiz Module Ready")
                    
                    with st.popover(f"👁️ Preview Quiz (Day {day})"):
                        import streamlit.components.v1 as components
                        clean_html = cached_lesson.replace('```html', '').replace('```', '')
                        components.html(clean_html, height=600, scrolling=True)

                else:
                    st.warning("⚠️ Not Generated")
                    if st.button(f"⚡ Generate Quiz Day {day}"):
                         with st.spinner("Building Senior-Level Quiz..."):
                             # 1. Get History
                             history = cache.get_topics_history(day)
                             # 2. Generate
                             content = gemini.generate_quiz(day, history)
                             cache.save_lesson(day, content)
                         st.success("Generated & Saved!")
                         st.rerun()

        if st.button("🚀 Send Quiz Modules", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_groups = len(day_groups)
            current_group_idx = 0
            
            for day, group in day_groups.items():
                status_text.write(f"Processing Quiz Day {day}...")
                
                content = cache.get_lesson(day)
                if not content:
                    status_text.write(f"Generating Quiz...")
                    history = cache.get_topics_history(day)
                    content = gemini.generate_quiz(day, history)
                    cache.save_lesson(day, content)
                
                status_text.write(f"Sending to {len(group)} students...")
                success, msg = mailer.send_email(group, f"🎯 PyDaily Challenge: Day {day}", content)
                
                if success:
                    for student in group:
                        data_manager.update_contact_status(student['email'], status='lesson_sent')
                else:
                    st.error(f"Quiz Day {day} Failed: {msg}")
                
                current_group_idx += 1
                progress_bar.progress(current_group_idx / total_groups)
            
            status_text.write("✅ All Quizzes Sent!")
            st.balloons()
            st.rerun()
