import streamlit as st
import pandas as pd
import time
from backend import data_manager

def run():
    # Inject Custom CSS
    try:
        with open('assets/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except: pass

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
                    # Generate Unique Temp Password
                    import random
                    import string
                    chars = string.ascii_letters + string.digits + "!@#"
                    temp_pass = ''.join(random.choice(chars) for _ in range(10))
                    
                    if data_manager.add_contact(name, email, temp_pass):
                        st.success(f"Added {name}!")
                        
                        # Send Welcome Email
                        with st.spinner("Sending Welcome Email..."):
                            from backend import email_service
                            config = data_manager.get_config()
                            mailer = email_service.EmailService(
                                config.get('email_address'), 
                                config.get('email_password'),
                                test_mode=config.get('test_mode', False),
                                admin_email=config.get('admin_email', '')
                            )
                            
                            ok, msg = mailer.send_welcome_email(email, name, temp_pass)
                            if ok:
                                st.toast("Welcome Email Sent! 🚀")
                            else:
                                st.error(f"Could not send email: {msg}")

                        time.sleep(1)
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

            # --- Password Reset (Admin Override) ---
            with st.expander("🔐 Security / Password Reset", expanded=False):
                st.caption(f"Manually set a new password for **{student.get('name')}**.")
                new_pass = st.text_input("New Password", type="password", key=f"pass_{selected_email}")
                if st.button("Update Password Now", type="secondary"):
                    if len(new_pass) < 6:
                        st.warning("Password min 6 chars")
                    else:
                        with st.spinner("Updating in Database..."):
                            success, msg = data_manager.admin_force_password_reset(selected_email, new_pass)
                            if success:
                                st.success("Password Updated!")
                            else:
                                st.error(f"Failed: {msg}")

            # --- Manual Status Edit (Power User) ---
            with st.expander("🛠️ Advanced Progress Edit", expanded=False):
                st.caption("Manually force a specific Day/Status (e.g. for testing or correcting errors).")
                with st.form("manual_edit"):
                    c_edit1, c_edit2 = st.columns(2)
                    new_day = c_edit1.number_input("Set Day", min_value=1, max_value=120, value=max(1, student.get('day', 1)))
                    new_status = c_edit2.selectbox("Set Status", ["pending", "lesson_sent", "complete", "paused"], index=["pending", "lesson_sent", "complete", "paused"].index(student.get('status', 'pending')))
                    
                    if st.form_submit_button("Force Update"):
                        result = data_manager.update_contact_status(selected_email, day=new_day, status=new_status)
                        if isinstance(result, tuple):
                             success, msg = result
                        else:
                             success, msg = result, "Unknown Error"

                        if success:
                            st.success(f"Updated: Day {new_day} | {new_status}")
                            st.rerun()
                        else:
                            st.error(f"Update failed: {msg}")

    else:
        st.info("No contacts yet. Add one above!")
