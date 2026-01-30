import streamlit as st
import time
from backend.db_supabase import SupabaseManager
from backend.lesson_manager import LessonManager
from views.student.components.countdown import render_countdown, should_show_countdown
from views.student.components.curriculum_preview import render_curriculum_preview
from views.student.components.starter_kit import render_starter_kit_download
from views.student.components.expert_kit import render_expert_kit_download
from views.student.components.welcome_tour import render_welcome_tour, should_show_tour
from views.student.components.skill_tree import render_skill_tree
from views.student.components.spaced_repetition import render_spaced_repetition
from views.student import feed

def run():
    st.markdown("""
    <style>
    .student-header {
        background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    .flashcard-title {
        background: -webkit-linear-gradient(45deg, #FF512F, #DD2476);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .badge {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # 1. Auth Check
    token = st.session_state.get("auth_token")
    if not token:
        st.error("Session expired. Please logout and login again.")
        return

    # 2. Data Fetch
    db = SupabaseManager()
    cache = LessonManager()
    profile = db.get_user_profile(token)
    
    if not profile:
        st.error("Could not load profile. Please contact support.")
        return

    # Prioritize full_name (Supabase Schema), fallback to name, then 'Student'
    name = profile.get('full_name', profile.get('name', 'Student'))
    current_day = profile.get('current_day', 1)
    status = profile.get('status', 'pending')
    
    # 2.5 Welcome Tour (First-time Day 1 users)
    if should_show_tour(profile):
        tour_active = render_welcome_tour()
        if tour_active:
            return  # Exit early - tour takes over the screen
    
    # 3. Header
    st.markdown(f"""
    <div class="student-header">
        <h1>🎓 Welcome, {name}!</h1>
        <p>You are currently on <b>Day {current_day}</b> of your Python journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="margin:0">📅 Day {current_day}</h3>
            <span style="color:gray">Current Level</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="margin:0">🔥 {status.title()}</h3>
            <span style="color:gray">Status</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        # Mock XP for now
        xp = (current_day - 1) * 100
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="margin:0">⭐ {xp} XP</h3>
            <span style="color:gray">Total Points</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    # 5. Progress Bar
    progress = min(current_day / 100.0, 1.0)
    st.progress(progress, text=f"Course Progress: {int(progress*100)}%")
    
    # 5.5 New Features Banner (for existing users Day 2+)
    if current_day > 1:
        if "dismissed_new_features" not in st.session_state:
            st.markdown("""
            <div style="background: linear-gradient(90deg, #3b82f6, #8b5cf6); 
                        border-radius: 12px; padding: 15px 20px; margin: 15px 0;
                        display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <span style="font-size: 1.2rem;">🎉 <strong>New Features!</strong></span>
                    <span style="opacity: 0.9; margin-left: 10px;">
                        Skill Tree, Bookmarks, Review Zone & more - explore below!
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✕ Dismiss", key="dismiss_banner"):
                st.session_state.dismissed_new_features = True
                st.rerun()
    
    # 5.6 Countdown Timer (only for Day 1 students waiting for lesson)
    if current_day == 1:
        lesson_exists = cache.get_lesson(1) is not None
        if not lesson_exists:
            st.write("")
            render_countdown()
            st.info("💡 **While you wait**, explore the tabs below to see what's coming!")
    
    # 5.7 Resource Hub (Kits for ALL users)
    with st.expander("📦 Resource Hub - Starter Kits & Roadmaps", expanded=(current_day <= 3)):
        col1, col2 = st.columns(2)
        with col1:
            render_starter_kit_download()
        with col2:
            render_expert_kit_download()
    
    st.divider()
    
    # 6. Interactive Learning Tabs
    st.write("")
    tab1, tab2, tab_feed, tab_practice, tab3 = st.tabs(["📚 Knowledge Vault", "🧠 Quiz Arena", "⚡ Scroll", "💻 Practice", "📊 Progress"])
    
    # --- TAB 1: KNOWLEDGE VAULT (Lesson Library) ---
    with tab1:
        st.subheader("📖 Lesson Library")
        st.markdown("Access any lesson from your journey so far.")
        
        # 1. Lesson Selector
        # Day list: 1 to current_day
        available_days = list(range(1, current_day + 1))
        
        # Check for jump from Review Zone
        jump_day = st.session_state.pop("jump_to_lesson", None)
        if jump_day and jump_day in available_days:
            default_index = available_days.index(jump_day)
            st.success(f"📖 Jumped to **Day {jump_day}** for review!")
        else:
            default_index = len(available_days) - 1  # Default to current day
        
        col_select, col_bookmark = st.columns([4, 1])
        with col_select:
            selected_day = st.selectbox("Select Lesson Day", available_days, index=default_index, format_func=lambda x: f"Day {x}")
        
        # Bookmark Toggle
        user_email = st.session_state.get("user_email", "")
        is_bookmarked = db.is_bookmarked(user_email, selected_day) if user_email else False
        
        with col_bookmark:
            st.write("")  # Spacer to align with selectbox
            if is_bookmarked:
                if st.button("⭐ Saved", key=f"bm_{selected_day}", use_container_width=True):
                    db.remove_bookmark(user_email, selected_day)
                    st.rerun()
            else:
                if st.button("☆ Save", key=f"bm_{selected_day}", use_container_width=True):
                    db.add_bookmark(user_email, selected_day)
                    st.toast(f"✅ Day {selected_day} bookmarked!")
                    st.rerun()
        
        # Show Bookmarks Quick Access
        bookmarks = db.get_bookmarks(user_email) if user_email else []
        if bookmarks:
            bookmark_days = [b['lesson_day'] for b in bookmarks]
            with st.expander(f"⭐ Your Bookmarks ({len(bookmarks)})"):
                for bm in bookmarks:
                    if st.button(f"📖 Day {bm['lesson_day']}", key=f"jump_{bm['lesson_day']}"):
                        st.session_state[f"selected_day_jump"] = bm['lesson_day']
                        st.rerun()
        
        # 2. Render Content
        cache = LessonManager()
        content = cache.get_lesson(selected_day)
        
        if content:
            st.divider()
            
            # Check if this is a Quiz (Day 3, 6...) or looks like JSON
            is_quiz_day = (selected_day % 3 == 0 and selected_day > 0)
            is_json = content.strip().startswith("{") or content.strip().startswith("[")
            
            if is_quiz_day or is_json:
                # Show Redirect Card
                st.info("🎯 **Interactive Quiz Detected**")
                st.markdown(f"""
                <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #166534; margin-top:0;">📝 Time to Test Your Skills!</h3>
                    <p style="color: #15803d;">This day features an interactive quiz instead of a reading lesson.</p>
                    <p>👉 <b>Navigate to the '🧠 Quiz Arena' tab above to take the quiz!</b></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # --- ANALYTICS: VIEW LESSON ---
                if f"log_lesson_{selected_day}" not in st.session_state:
                    db.log_activity(st.session_state.get("user_email", "unknown"), "VIEW_LESSON", {"day": selected_day})
                    st.session_state[f"log_lesson_{selected_day}"] = True
                
                # Render Standard Lesson HTML
                clean_html = content.replace('```html', '').replace('```', '')
                import streamlit.components.v1 as components
                components.html(clean_html, height=700, scrolling=True)
                
                # --- DEEP DIVE SECTION ---
                from backend import curriculum
                topic_name = curriculum.TOPICS.get(selected_day, "")
                deep_dive = curriculum.get_deep_dive_attrs(selected_day, topic_name)
                
                if deep_dive:
                    dd_url, dd_source = deep_dive
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%); 
                                border-radius: 16px; padding: 24px; margin-top: 20px;
                                border: 1px solid #3b82f6;">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <span style="font-size: 2.5rem;">🔗</span>
                            <div>
                                <div style="font-size: 1.2rem; font-weight: 700; color: white;">
                                    📚 Deep Dive
                                </div>
                                <div style="color: #e0e7ff; margin-top: 5px;">
                                    Want to learn more? Check out this curated resource:
                                </div>
                            </div>
                        </div>
                        <a href="{dd_url}" target="_blank" rel="noopener" 
                           style="display: inline-block; margin-top: 15px; 
                                  background: white; color: #1e40af; 
                                  padding: 12px 24px; border-radius: 8px;
                                  text-decoration: none; font-weight: 600;
                                  transition: transform 0.2s;">
                            🚀 Explore on {dd_source} →
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"Day {selected_day} content not found in cache. Ask your Admin to generate it!")

    # --- TAB 2: QUIZ ARENA (Interactive) ---
    with tab2:
        st.subheader("⚔️ The Arena")
        st.markdown("Test your skills on checkpoint days.")
        
        # 1. Identify Quiz Days (Every 3 days)
        quiz_days = [d for d in range(1, current_day + 1) if d % 3 == 0]
        
        if not quiz_days:
            st.info("No Quizzes unlocked yet! Keep going until Day 3.")
        else:
            # Quiz Selector
            selected_quiz_day = st.selectbox("Select Quiz", quiz_days, index=len(quiz_days)-1, format_func=lambda x: f"Day {x} Checkpoint")
            
            # --- ANALYTICS: START QUIZ ---
            # Debounce per session/quiz combination
            if f"log_quiz_start_{selected_quiz_day}" not in st.session_state:
                 db.log_activity(st.session_state["user_email"], "START_QUIZ", {"day": selected_quiz_day})
                 st.session_state[f"log_quiz_start_{selected_quiz_day}"] = True

            # 2. Get Quiz Content
            quiz_content = cache.get_lesson(selected_quiz_day)
            
            if not quiz_content:
                st.warning("Quiz content not found.")
            else:
                # 3. Parse JSON
                import json
                try:
                    # Robust JSON parsing (handle if it's wrapped in strings or markdown)
                    clean_json = quiz_content.replace('```json', '').replace('```', '').strip()
                    quiz_data = json.loads(clean_json)
                    
                    st.divider()
                    st.markdown(f"### 🎯 {quiz_data.get('title', 'Quiz')}")
                    
                    # 4. Render Form
                    with st.form(f"quiz_form_{selected_quiz_day}"):
                        score = 0
                        total = len(quiz_data.get('questions', []))
                        user_answers = {}
                        
                        for q in quiz_data.get('questions', []):
                            st.markdown(f"**Q{q.get('id')}: {q.get('question')}**")
                            # Radio button for options
                            user_val = st.radio(
                                "Select Answer:", 
                                q.get('options', []), 
                                key=f"q_{q.get('id')}_{selected_quiz_day}",
                                label_visibility="collapsed"
                            )
                            user_answers[q.get('id')] = user_val
                            st.write("") # Spacer
                            
                        submit = st.form_submit_button("Detailed Assessment ->")
                        
                        if submit:
                            # 1. Grading Logic
                            correct_count = 0
                            
                            for q in quiz_data.get('questions', []):
                                q_id = q.get('id')
                                u_ans = user_answers.get(q_id)
                                r_ans = q.get('answer')
                                if u_ans == r_ans:
                                    correct_count += 1
                            
                            # 2. Save to DB
                            with st.spinner("Saving Results..."):
                                success, msg = db.save_quiz_result(token, selected_quiz_day, correct_count, total, user_answers)
                                if not success:
                                    st.error(f"Error saving result: {msg}")
                                else:
                                    # --- ANALYTICS: SUBMIT QUIZ ---
                                    db.log_activity(st.session_state["user_email"], "SUBMIT_QUIZ", {
                                        "day": selected_quiz_day, 
                                        "score": correct_count, 
                                        "total": total
                                    })

                            # 3. Show Feedback
                            st.write("---")
                            st.subheader("📊 Results")
                            
                            for q in quiz_data.get('questions', []):
                                q_id = q.get('id')
                                u_ans = user_answers.get(q_id)
                                r_ans = q.get('answer')
                                
                                if u_ans == r_ans:
                                    st.success(f"✅ Q{q_id}: Correct!")
                                else:
                                    st.error(f"❌ Q{q_id}: Incorrect. You chose '{u_ans}'.")
                                    st.markdown(f"**Correct Answer:** {r_ans}")
                                    st.info(f"💡 **Explanation:** {q.get('explanation')}")
                                    
                            st.metric("Final Score", f"{correct_count} / {total}")
                            
                            if correct_count == total:
                                st.balloons()
                            elif correct_count >= total / 2:
                                st.snow()
                                
                except json.JSONDecodeError:
                    st.error("⚠️ Error loading Interactive Quiz. It might be in the old legacy format.")
                    st.expander("View Legacy Content").code(quiz_content)
                    
    # --- TAB FEED: INFINITE SCROLL ---
    with tab_feed:
        feed.run(current_day)

    # --- TAB 3: PRACTICE PROGRAMS (Flashcard Gym) ---
    with tab_practice:
        st.subheader("🏋️ Coding Gym")
        st.markdown("Practice makes perfect. Choose your training mode.")
        
        tab_drill, tab_boss, tab_review = st.tabs(["🧩 Daily Drill", "🔥 Boss Battles", "🧠 Review Zone"])
        
        # --- TAB A: DAILY DRILL (Existing) ---
        with tab_drill:
            if current_day > 0:
                # 1. Day Selector
                available_days = list(range(1, current_day + 1))
                sel_day = st.selectbox("Select Drill Day:", reversed(available_days), index=0, key="drill_day_sel")
                
                # 2. Fetch Items
                items = cache.extract_practice_items(sel_day)
                
                if not items:
                    st.info("No specific practice problems found for this day.")
                else:
                    # 3. Carousel Logic
                    idx_key = f"pract_idx_{sel_day}"
                    if idx_key not in st.session_state:
                        st.session_state[idx_key] = 0
                    
                    curr_idx = st.session_state[idx_key]
                    item = items[curr_idx]
                    
                    # 4. The Flashy Card
                    is_challenge = "Daily Challenge" in item['title']
                    icon = "🔥" if is_challenge else "💠"
                    
                    with st.container(border=True):
                        # Custom Gradient Title with Icon embedded
                        st.markdown(f'<div class="flashcard-title">{icon} {item["title"]}</div>', unsafe_allow_html=True)
                        
                        # Metadata Badge
                        st.markdown(f'<span class="badge">Problem {curr_idx + 1} of {len(items)}</span>', unsafe_allow_html=True)
                        st.markdown("---")
                        
                        # Content
                        st.markdown(item['instruction']) # Support Markdown
                        
                    # 5. Navigation
                    c1, c2, c3 = st.columns([1, 2, 1])
                    with c1:
                        if st.button("⬅️ Previous", key=f"prev_{sel_day}", disabled=(curr_idx == 0)):
                             st.session_state[idx_key] -= 1
                             st.rerun()
                    with c3:
                        if st.button("Next ➡️", key=f"next_{sel_day}", disabled=(curr_idx == len(items) - 1)):
                             st.session_state[idx_key] += 1
                             st.rerun()
            else:
                 st.info("Complete Day 1 to unlock the Gym!")

        # --- TAB B: BOSS BATTLES (New) ---
        with tab_boss:
            st.markdown("### 🔥 The Boss Arena")
            st.markdown("Real-world scenarios. No hand-holding. For the ambitious.")
            
            if current_day > 0:
                available_days_boss = list(range(1, current_day + 1))
                sel_day_boss = st.selectbox("Select Boss Day:", reversed(available_days_boss), index=0, key="boss_day_sel")
                
                # Fetch Battles
                battles = db.get_boss_battles(sel_day_boss)
                
                if not battles:
                    st.info(f"🛡️ No Boss Battles detected for Day {sel_day_boss} yet. The Arena is quiet...")
                else:
                    for i, battle in enumerate(battles):
                        with st.expander(f"⚔️ {battle['title']}"):
                            st.markdown(f"**Scenario:** {battle['scenario']}")
                            
                            st.markdown("#### 📋 Requirements:")
                            for req in battle.get('requirements', []):
                                st.markdown(f"- [ ] {req}")
                                
                            if battle.get('hints'):
                                if st.checkbox("Show Hints 💡", key=f"hint_{sel_day_boss}_{i}"):
                                    for h in battle['hints']:
                                        st.markdown(f"- *{h}*")
            else:
                st.warning("Complete Day 1 to enter the Arena.")
        
        # --- TAB C: REVIEW ZONE (Spaced Repetition) ---
        with tab_review:
            if current_day >= 7:
                render_spaced_repetition(current_day)
            else:
                st.info("🕐 **Review Zone unlocks at Day 7**")
                st.markdown("Come back once you've completed a full week of learning!")
                
    # --- TAB 4: PROGRESS ---
    with tab3:
        st.subheader("📊 Your Learning Curve")
        
        # Skill Tree (Interactive constellation visualization)
        render_skill_tree(current_day)
        
        st.divider()
        
        # Curriculum Roadmap (Collapsible for experienced users, expanded for new users)
        roadmap_expanded = current_day <= 7  # Auto-expand for first week
        with st.expander("🗺️ View Phase Details", expanded=roadmap_expanded):
            render_curriculum_preview(current_day)
        
        # 1. Fetch Granular History
        attempts = db.get_student_attempts(token)
        
        if not attempts:
            st.info("No quiz history found. Take your first quiz in the Arena!")
        else:
            import pandas as pd
            import altair as alt
            
            # 2. Process Data
            data = []
            for item in attempts:
                score = item.get('score', 0)
                total = item.get('total', 25) # Note: DB column is 'total' in attempts table
                pct = (score / total) * 100 if total > 0 else 0
                
                # Handle timestamp
                ts = item.get('submitted_at')
                # format timestamp nicely
                
                data.append({
                    "Day Name": f"Day {item.get('day')}",
                    "Day": item.get('day'),
                    "Score": score,
                    "Total": total,
                    "Percentage": pct,
                    "Timestamp": ts
                })
            
            df = pd.DataFrame(data)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            
            # 3. Metrics (Aggregated)
            # Best Score per Day
            best_scores = df.groupby('Day')['Percentage'].max()
            avg_best = best_scores.mean()
            total_quizzes = df['Day'].nunique()
            total_attempts = len(df)
            
            m1, m2, m3 = st.columns(3)
            with m1: st.metric("Quizzes Mastered", total_quizzes, help="Unique Days Completed")
            with m2: st.metric("Total Attempts", total_attempts, help="Total Simulations Run")
            with m3: st.metric("Avg Proficiency", f"{avg_best:.1f}%", help="Average of your BEST score for each day")
            
            st.divider()
            
            # 4. Creative Visualization: Inter-Day Progress (Scatter + Line)
            st.markdown("#### 📈 Skill Trajectory")
            st.caption("See how your score improves with every attempt.")
            
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X('Timestamp', title='Time', axis=alt.Axis(format='%b %d %H:%M')),
                y=alt.Y('Percentage', title='Score (%)', scale=alt.Scale(domain=[0, 100])),
                color='Day Name',
                tooltip=['Day Name', 'Score', 'Total', 'Percentage', 'Timestamp']
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            
            # 5. Detailed Log (Grouped by Day)
            st.markdown("#### 📜 Attempt Log")
            
            if df.empty:
                st.info("No quizzes taken yet.")
            else:
                # Group by Day (Sort by Day Descending)
                days = sorted(df['Day'].unique(), reverse=True)
                
                for day in days:
                    day_df = df[df['Day'] == day].sort_values('Timestamp', ascending=False)
                    
                    # Summary Metrics for this Day
                    best = day_df['Percentage'].max()
                    attempts = len(day_df)
                    
                    # Color code the header
                    icon = "⭐" if best >= 80 else "📈" if best >= 50 else "🚧"
                    
                    with st.expander(f"{icon} **Day {day} Quiz**: {best:.0f}% Best Score ({attempts} Attempts)"):
                        st.dataframe(
                            day_df[['Percentage', 'Score', 'Timestamp']],
                            use_container_width=True,
                            column_config={
                                "Percentage": st.column_config.ProgressColumn(
                                    "Score (%)", format="%.1f%%", min_value=0, max_value=100
                                ),
                                "Timestamp": st.column_config.DatetimeColumn(
                                    "Submitted At", format="MMM D, h:mm a"
                                )
                            },
                            hide_index=True
                        )
