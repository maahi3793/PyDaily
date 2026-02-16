import streamlit as st
import time
from backend.db_supabase import SupabaseManager

def run():
    st.markdown("""
    <style>
    .pref-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
        max-width: 600px;
        margin: 0 auto;
    }
    .hero-text {
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 1. Get Email from Query Param
    query_params = st.query_params
    email = query_params.get("email", None)
    
    # Handle single string vs list return
    if isinstance(email, list): email = email[0]
    
    st.markdown('<div class="hero-text"><h1>🔕 Email Preferences</h1><p>Manage what you receive from PyDaily.</p></div>', unsafe_allow_html=True)

    if not email:
        st.error("Invalid Link. Please use the link from your email footer.")
        return

    db = SupabaseManager()
    
    # 2. Fetch Current Prefs
    with st.spinner("Loading preferences..."):
        # We need a method to get prefs by email (using Admin key internally if needed)
        prefs = db.get_preferences(email)
        
    if not prefs:
        st.error(f"Could not find subscription data for {email}. Please contact support.")
        return
        
    # 3. Form
    st.markdown(f'<div class="pref-card">', unsafe_allow_html=True)
    st.write(f"Settings for: **{email}**")
    st.divider()
    
    with st.form("pref_form"):
        st.subheader("I want to receive:")
        
        # Checkboxes
        col1, col2 = st.columns(2)
        with col1:
             sub_morning = st.checkbox("☀️ Morning Motivation", value=prefs.get('sub_morning', True), help="Daily quote to start your day.")
        with col2:
             sub_evening = st.checkbox("🌙 Evening Lesson", value=prefs.get('sub_evening', True), help="Your daily Python micro-challenge.")
             
        st.write("")
        st.write("")
        
        submitted = st.form_submit_button("Update Preferences", type="primary", use_container_width=True)
        
    # 4. Unsubscribe All Logic
    if st.button("🚫 Unsubscribe from Everything", type="secondary", use_container_width=True):
        with st.spinner("Unsubscribing..."):
            success, msg = db.update_preferences(email, False, False)
            if success:
                st.success("You have been unsubscribed from all emails.")
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"Error: {msg}")
                
    if submitted:
        with st.spinner("Saving..."):
            success, msg = db.update_preferences(email, sub_morning, sub_evening)
            if success:
                st.success("Preferences saved successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Error: {msg}")

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back to home
    st.write("")
    if st.button("← Back to PyDaily Login"):
        # Clear query params to go back to main
        st.query_params.clear()
        st.rerun()
