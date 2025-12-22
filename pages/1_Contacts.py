import streamlit as st
import pandas as pd
from backend import data_manager

st.set_page_config(page_title="Contacts", page_icon="👥")

# Inject Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# HERO HEADER
st.markdown("""
<div class="hero-header">
    <div class="hero-title">Student Roster</div>
    <div class="hero-subtitle">Add new students, track progress, and manage active enrollments</div>
</div>
""", unsafe_allow_html=True)

# Form
with st.expander("➕ Add New Student", expanded=False):
    with st.form("add_contact"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name")
        email = c2.text_input("Email")
        # Spacer
        st.write("")
        submitted = st.form_submit_button("Add to Cohort", type="primary", use_container_width=True)
        
        if submitted:
            if name and email:
                if data_manager.add_contact(name, email):
                    st.success(f"Added {name}!")
                    st.rerun()
                else:
                    st.error("Email already exists!")
            else:
                st.warning("Please fill both fields.")

st.write("") # Spacer

# List
contacts = data_manager.get_contacts()

if contacts:
    st.markdown("### 📋 Student Roster")
    
    # metrics
    df = pd.DataFrame(contacts)
    
    # Styled Dataframe
    st.dataframe(
        df, 
        use_container_width=True,
        column_config={
            "day": st.column_config.ProgressColumn("Progress", min_value=0, max_value=100, format="Day %d"),
            "status": st.column_config.SelectboxColumn("Status", options=['pending', 'lesson_sent', 'complete', 'paused'])
        }
    )
    
    st.divider()
    st.subheader("🛠️ Manage Student")
    
    valid_contacts = [c for c in contacts if isinstance(c, dict) and c.get('email')]
    selected_email = st.selectbox("Select Student", [c['email'] for c in valid_contacts], format_func=lambda x: f"{x} - {[c['name'] for c in contacts if c['email']==x][0]}")
    
    if selected_email:
        # Get current student obj
        student = [c for c in contacts if c['email'] == selected_email][0]
        
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.metric("Current Day", student.get('day', 1))
        with c2:
            st.metric("Status", student.get('status', 'unknown'))
            
        st.write("Actions:")
        b1, b2, b3, b4 = st.columns(4)
        
        if b1.button("🔄 Reset to Day 1", use_container_width=True):
            data_manager.update_contact_status(selected_email, day=1, status='pending')
            st.success("Reset!")
            st.rerun()
            
        if b2.button("⏩ Skip Next Day", use_container_width=True):
            data_manager.update_contact_status(selected_email, day=student.get('day', 1) + 1)
            st.success("Skipped!")
            st.rerun()

        if b3.button("⏸️ Pause/Resume", use_container_width=True):
            new_status = 'paused' if student.get('status') != 'paused' else 'pending'
            data_manager.update_contact_status(selected_email, status=new_status)
            st.success(f"Set to {new_status}!")
            st.rerun()
            
        if b4.button("🗑️ Delete User", type="primary", use_container_width=True):
            data_manager.delete_contact(selected_email)
            st.warning("Deleted.")
            st.rerun()

else:
    st.info("No contacts yet. Add one above!")
