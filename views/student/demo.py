"""
Demo Mode Dashboard — Read-only replica of the Student Dashboard.
Restricted to Days 1-3. Quiz works interactively but nothing saves to DB.
"""
import streamlit as st
from backend.lesson_manager import LessonManager

DEMO_MAX_DAY = 3

def run():
    # --- CSS (Same as student dashboard) ---
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
    .demo-banner {
        background: linear-gradient(90deg, #f59e0b, #ef4444);
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.title("🎮 Demo Mode")
        st.caption("You are exploring PyDaily as a guest.")
        st.divider()
        if st.button("← Back to Login", use_container_width=True):
            st.session_state["role"] = "guest"
            st.rerun()
        st.divider()
        if st.button("🚀 Sign Up Now", type="primary", use_container_width=True):
            st.session_state["role"] = "guest"
            st.rerun()

    # --- Demo Banner ---
    st.markdown("""
    <div class="demo-banner">
        <span>🎯 Demo Mode — You're previewing Days 1-3. Sign up to unlock 200+ lessons, quizzes & boss battles!</span>
    </div>
    """, unsafe_allow_html=True)

    # Sign up button right after banner
    if st.button("✨ Sign Up Free — Unlock Everything", type="primary", use_container_width=True):
        st.session_state["role"] = "guest"
        st.rerun()

    # --- Header (mirrors student dashboard) ---
    name = "Explorer"
    current_day = DEMO_MAX_DAY

    st.markdown(f"""
    <div class="student-header">
        <h1>🎓 Welcome, {name}!</h1>
        <p>You are currently on <b>Day {current_day}</b> of your Python journey.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="margin:0">📅 Day {current_day}</h3>
            <span style="color:gray">Current Level</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h3 style="margin:0">🔥 Active</h3>
            <span style="color:gray">Status</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        xp = (current_day - 1) * 100
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="margin:0">⭐ {xp} XP</h3>
            <span style="color:gray">Total Points</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Progress Bar
    progress = min(current_day / 100.0, 1.0)
    st.progress(progress, text=f"Course Progress: {int(progress*100)}%")

    st.divider()

    # --- Tabs (same as real dashboard) ---
    tab1, tab2, tab_practice, tab3 = st.tabs(["📚 Knowledge Vault", "🧠 Quiz Arena", "💻 Practice", "📊 Progress"])

    cache = LessonManager()

    # === TAB 1: KNOWLEDGE VAULT ===
    with tab1:
        st.subheader("📖 Lesson Library")
        st.markdown("Access any lesson from your journey so far.")

        available_days = list(range(1, current_day + 1))
        selected_day = st.selectbox(
            "Select Lesson Day", available_days,
            index=len(available_days) - 1,
            format_func=lambda x: f"Day {x}"
        )

        content = cache.get_lesson(selected_day)

        if content:
            st.divider()
            is_quiz_day = (selected_day % 3 == 0 and selected_day > 0)
            is_json = content.strip().startswith("{") or content.strip().startswith("[")

            if is_quiz_day or is_json:
                st.info("🎯 **Interactive Quiz Detected**")
                st.markdown("""
                <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #166534; margin-top:0;">📝 Time to Test Your Skills!</h3>
                    <p style="color: #15803d;">This day features an interactive quiz instead of a reading lesson.</p>
                    <p>👉 <b>Navigate to the '🧠 Quiz Arena' tab above to take the quiz!</b></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                clean_html = content.replace('```html', '').replace('```', '')
                import streamlit.components.v1 as components
                components.html(clean_html, height=700, scrolling=True)

                # Deep Dive Link
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
                                  text-decoration: none; font-weight: 600;">
                            🚀 Explore on {dd_source} →
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"Day {selected_day} content is being generated. Check back soon!")

    # === TAB 2: QUIZ ARENA (Interactive, No Save) ===
    with tab2:
        st.subheader("⚔️ The Arena")
        st.markdown("Test your skills on checkpoint days.")

        quiz_days = [d for d in range(1, current_day + 1) if d % 3 == 0]

        if not quiz_days:
            st.info("No Quizzes unlocked yet! Keep going until Day 3.")
        else:
            selected_quiz_day = st.selectbox(
                "Select Quiz", quiz_days,
                index=len(quiz_days) - 1,
                format_func=lambda x: f"Day {x} Checkpoint"
            )

            quiz_content = cache.get_lesson(selected_quiz_day)

            if not quiz_content:
                st.warning("Quiz content not found.")
            else:
                import json
                try:
                    clean_json = quiz_content.replace('```json', '').replace('```', '').strip()
                    quiz_data = json.loads(clean_json)

                    st.divider()
                    st.markdown(f"### 🎯 {quiz_data.get('title', 'Quiz')}")

                    with st.form(f"demo_quiz_form_{selected_quiz_day}"):
                        score = 0
                        total = len(quiz_data.get('questions', []))
                        user_answers = {}

                        for q in quiz_data.get('questions', []):
                            st.markdown(f"**Q{q.get('id')}: {q.get('question')}**")
                            user_val = st.radio(
                                "Select Answer:",
                                q.get('options', []),
                                key=f"demo_q_{q.get('id')}_{selected_quiz_day}",
                                label_visibility="collapsed"
                            )
                            user_answers[q.get('id')] = user_val
                            st.write("")

                        submit = st.form_submit_button("Submit Quiz →")

                        if submit:
                            correct_count = 0
                            for q in quiz_data.get('questions', []):
                                q_id = q.get('id')
                                u_ans = user_answers.get(q_id)
                                r_ans = q.get('answer')
                                if u_ans == r_ans:
                                    correct_count += 1

                            # Show Feedback (NO DB SAVE)
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

                            # CTA after quiz
                            st.divider()
                            st.markdown("""
                            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); border-radius: 12px; color: white;">
                                <h3 style="margin:0;">🎉 Enjoyed the quiz?</h3>
                                <p>Sign up free to track your scores, unlock 200+ lessons, and get personalized AI feedback!</p>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("🚀 Sign Up Now — It's Free!", key="cta_after_quiz"):
                                st.session_state["role"] = "guest"
                                st.rerun()

                except json.JSONDecodeError:
                    st.error("⚠️ Error loading quiz data.")

    # === TAB 3: PRACTICE (Locked Preview) ===
    with tab_practice:
        st.subheader("🏋️ Coding Gym")
        st.markdown("Practice makes perfect. Choose your training mode.")

        tab_drill, tab_boss = st.tabs(["🧩 Daily Drill", "🔥 Boss Battles"])

        with tab_drill:
            if current_day > 0:
                available_days = list(range(1, current_day + 1))
                sel_day = st.selectbox("Select Drill Day:", reversed(available_days), index=0, key="demo_drill_day")

                items = cache.extract_practice_items(sel_day)

                if not items:
                    st.info("No specific practice problems found for this day.")
                else:
                    idx_key = f"demo_pract_idx_{sel_day}"
                    if idx_key not in st.session_state:
                        st.session_state[idx_key] = 0

                    curr_idx = st.session_state[idx_key]
                    item = items[curr_idx]

                    is_challenge = "Daily Challenge" in item['title']
                    icon = "🔥" if is_challenge else "💠"

                    with st.container(border=True):
                        st.markdown(f'<div class="flashcard-title">{icon} {item["title"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<span class="badge">Problem {curr_idx + 1} of {len(items)}</span>', unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown(item['instruction'])

                    c1, c2, c3 = st.columns([1, 2, 1])
                    with c1:
                        if st.button("⬅️ Previous", key=f"demo_prev_{sel_day}", disabled=(curr_idx == 0)):
                            st.session_state[idx_key] -= 1
                            st.rerun()
                    with c3:
                        if st.button("Next ➡️", key=f"demo_next_{sel_day}", disabled=(curr_idx == len(items) - 1)):
                            st.session_state[idx_key] += 1
                            st.rerun()

        with tab_boss:
            st.markdown("### 🔥 The Boss Arena")
            st.markdown("Real-world scenarios. No hand-holding. For the ambitious.")
            st.info("🔒 **Boss Battles unlock after signup.** Sign up to access job-ready coding challenges!")
            if st.button("🚀 Unlock Boss Battles — Sign Up Free", key="cta_boss"):
                st.session_state["role"] = "guest"
                st.rerun()

    # === TAB 4: PROGRESS (Locked Preview) ===
    with tab3:
        st.subheader("📊 Your Learning Curve")

        # Show curriculum preview
        from views.student.components.curriculum_preview import render_curriculum_preview
        with st.expander("🗺️ View Phase Details", expanded=True):
            render_curriculum_preview(current_day)

        st.divider()
        st.info("🔒 **Detailed progress tracking, skill tree, and quiz history unlock after signup.**")

        # Fake metrics preview
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Quizzes Mastered", "—")
        with m2: st.metric("Total Attempts", "—")
        with m3: st.metric("Avg Proficiency", "—")

        st.divider()
        if st.button("🚀 Sign Up to Track Your Progress", type="primary", use_container_width=True, key="cta_progress"):
            st.session_state["role"] = "guest"
            st.rerun()
