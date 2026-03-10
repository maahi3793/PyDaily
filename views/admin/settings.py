import streamlit as st
from backend import data_manager, email_service

def run():
    # Inject Custom CSS
    try:
        with open('assets/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except: pass

    # HERO HEADER
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">System Settings</div>
        <div class="hero-subtitle">Configure API keys, email credentials, and administrative controls</div>
    </div>
    """, unsafe_allow_html=True)

    config = data_manager.get_config()

    with st.form("config"):
        # Group inputs in columns for cleaner look
        st.markdown("### 🔑 API Keys")
        gemini_key = st.text_input("Gemini API Key", value=config.get('gemini_key', ''), type="password")
        
        st.write("")
        st.markdown("### 📧 Email Credentials")
        st.caption("Use an **App Password** from your Google Account settings, NOT your main password.")
        
        col1, col2 = st.columns(2)
        email_addr = col1.text_input("Sender Email Address", value=config.get('email_address', ''))
        email_pass = col2.text_input("App Password", value=config.get('email_password', ''), type="password")
        
        st.write("")
        st.markdown("### 🧪 Admin Sandbox")
        st.info("When Test Mode is ON, all emails are sent ONLY to the Admin Email. Useful for dry-runs.")
        
        c1, c2 = st.columns([1, 2])
        test_mode = c1.checkbox("Enable Test Mode", value=config.get('test_mode', False))
        admin_email = c2.text_input("Admin Email (for testing)", value=config.get('admin_email', ''))

        st.write("")
        saved = st.form_submit_button("💾 Save Settings", type="primary", use_container_width=True)
        
        if saved:
            data_manager.save_config(gemini_key, email_addr, email_pass, test_mode, admin_email)
            st.success(f"Settings saved! Test Mode is {'ON' if test_mode else 'OFF'}.")

    st.divider()

    st.subheader("Connection Test")
    if st.button("🔌 Test Email Connection", use_container_width=True):
        if not email_addr or not email_pass:
            st.error("Please save credentials first.")
        else:
            mailer = email_service.EmailService(email_addr, email_pass)
            success, msg = mailer.test_connection()
            if success:
                st.success(msg)
            else:
                st.error(f"Connection Failed: {msg}")

    st.subheader("Database Diagnostics")
    if st.button("🩺 Test Analytics Logging"):
        with st.spinner("Wait..."):
             db = data_manager.db
             if not db.admin_supabase:
                 st.error("❌ Admin Supabase Client is NONE. Check SUPABASE_SERVICE_KEY in .env")
             else:
                 st.write("✅ Admin Client Initialized.")
                 try:
                     # Try explicit insert
                     res = db.admin_supabase.table('activity_logs').insert({
                         "user_email": "admin@test.com", 
                         "action": "TEST_DIAGNOSTIC", 
                         "details": {"source": "settings_page"}
                     }).execute()
                     st.success("✅ Insert Successful! Check the dashboard now.")
                     st.json(res.data)
                 except Exception as e:
                     st.error(f"❌ Insert Failed: {e}")
                     # Print full trace to stdout for backend logs
                     import traceback
                     traceback.print_exc()
