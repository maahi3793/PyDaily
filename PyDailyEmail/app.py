import streamlit as st
from backend import data_manager, gemini_service, email_service
import datetime

st.set_page_config(page_title="PyDaily Admin", page_icon="🐍", layout="wide")

st.title("🐍 PyDaily Admin Dashboard")

# Load Config & State
config = data_manager.get_config()
state = data_manager.get_state()
contacts = data_manager.get_contacts()

if not config.get('gemini_key') or not config.get('email_address'):
    st.warning("⚠️ Please configure your API Keys and Email in 'Settings' first!")
    st.stop()

# Helpers
gemini = gemini_service.GeminiService(config['gemini_key'])
mailer = email_service.EmailService(config['email_address'], config['email_password'])

# --- Sidebar info ---
st.sidebar.header("Status")
st.sidebar.metric("Current Day", state['current_day'])
st.sidebar.metric("Subscribers", len(contacts))
if state['last_run']:
    st.sidebar.caption(f"Last Run: {state['last_run']}")

# --- Main Content ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"📝 Preview: Day {state['current_day']}")
    
    # Session State to hold generated content so it doesn't vanish on reru
    if 'preview_content' not in st.session_state:
        st.session_state.preview_content = ""

    if st.button("✨ Generate Preview"):
        with st.spinner("Asking Gemini..."):
            content = gemini.generate_lesson(state['current_day'])
            st.session_state.preview_content = content
    
    if st.session_state.preview_content:
        st.markdown(st.session_state.preview_content, unsafe_allow_html=True)
        
        st.divider()
        
        # Sending Logic
        if st.button("🚀 Send to All Subscribers", type="primary"):
            if not contacts:
                st.error("No subscribers found! Add some in 'Contacts'.")
            else:
                with st.spinner("Sending emails..."):
                    success, msg = mailer.send_email(
                        contacts, 
                        f"🐍 PyDaily: Day {state['current_day']}", 
                        st.session_state.preview_content
                    )
                    
                    if success:
                        st.success(msg)
                        # granular update
                        state['current_day'] += 1
                        state['last_run'] = str(datetime.datetime.now())
                        data_manager.update_state(state['current_day'], state['last_run'])
                        st.balloons()
                        # clear preview
                        st.session_state.preview_content = ""
                        st.rerun()
                    else:
                        st.error(f"Failed: {msg}")

with col2:
    st.info("""
    **How to use:**
    1. Click 'Generate Preview' to see what Gemini writes for today.
    2. Read it over.
    3. Click 'Send' to dispatch to your list.
    
    The 'Current Day' will auto-increment after a successful send.
    """)
    
    st.subheader("Manual Override")
    new_day = st.number_input("Jump to Day", min_value=1, value=state['current_day'])
    if st.button("Set Day"):
        data_manager.update_state(day=new_day)
        st.success(f"Jumped to Day {new_day}")
        st.rerun()
