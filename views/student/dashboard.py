import streamlit as st
import time
from backend.db_supabase import SupabaseManager
from backend.lesson_manager import LessonManager

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
    </style>
    """, unsafe_allow_html=True)

    # 1. Auth Check
    token = st.session_state.get("auth_token")
    if not token:
        st.error("Session expired. Please logout and login again.")
        return

    # 2. Data Fetch
    db = SupabaseManager()
    profile = db.get_user_profile(token)
    
    if not profile:
        st.error("Could not load profile. Please contact support.")
        return

    # Prioritize full_name (Supabase Schema), fallback to name, then 'Student'
    name = profile.get('full_name', profile.get('name', 'Student'))
    current_day = profile.get('current_day', 1)
    status = profile.get('status', 'pending')
    
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
    
    st.divider()
    
    # 6. Interactive Learning Tabs
    st.write("")
    tab1, tab2 = st.tabs(["📚 Knowledge Vault", "🧠 Quiz Arena"])
    
    # --- TAB 1: KNOWLEDGE VAULT (Lesson Library) ---
    with tab1:
        st.subheader("📖 Lesson Library")
        st.markdown("Access any lesson from your journey so far.")
        
        # 1. Lesson Selector
        # Day list: 1 to current_day
        available_days = list(range(1, current_day + 1))
        
        # Default to current day
        selected_day = st.selectbox("Select Lesson Day", available_days, index=len(available_days)-1, format_func=lambda x: f"Day {x}")
        
        # 2. Render Content
        cache = LessonManager()
        content = cache.get_lesson(selected_day)
        
        if content:
            st.divider()
            # Clean Markdown if needed
            clean_html = content.replace('```html', '').replace('```', '')
            import streamlit.components.v1 as components
            components.html(clean_html, height=700, scrolling=True)
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
