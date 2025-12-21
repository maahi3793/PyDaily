import streamlit as st
from backend import data_manager, email_service

st.set_page_config(page_title="Settings", page_icon="⚙️")

st.title("⚙️ Settings")

config = data_manager.get_config()

with st.form("config"):
    st.markdown("### 🔑 API Keys")
    gemini_key = st.text_input("Gemini API Key", value=config.get('gemini_key', ''), type="password")
    
    st.markdown("### 📧 Email Credentials")
    st.markdown("*Use an **App Password** from your Google Account settings, NOT your main password.*")
    email_addr = st.text_input("Sender Email Address", value=config.get('email_address', ''))
    email_pass = st.text_input("App Password", value=config.get('email_password', ''), type="password")
    
    saved = st.form_submit_button("Save Settings")
    
    if saved:
        data_manager.save_config(gemini_key, email_addr, email_pass)
        st.success("Settings saved successfully!")

st.divider()

st.subheader("Connection Test")
if st.button("Test Email Connection"):
    if not email_addr or not email_pass:
        st.error("Please save credentials first.")
    else:
        mailer = email_service.EmailService(email_addr, email_pass)
        success, msg = mailer.test_connection()
        if success:
            st.success(msg)
        else:
            st.error(f"Connection Failed: {msg}")
