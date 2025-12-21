import streamlit as st
import pandas as pd
from backend import data_manager

st.set_page_config(page_title="Contacts", page_icon="👥")

st.title("👥 Subscriber Management")

# Form
with st.form("add_contact"):
    c1, c2 = st.columns(2)
    name = c1.text_input("Name")
    email = c2.text_input("Email")
    submitted = st.form_submit_button("Add Contact")
    
    if submitted:
        if name and email:
            if data_manager.add_contact(name, email):
                st.success(f"Added {name}!")
                st.rerun()
            else:
                st.error("Email already exists!")
        else:
            st.warning("Please fill both fields.")

st.divider()

# List
contacts = data_manager.get_contacts()

if contacts:
    # Convert to DataFrame for nicer display
    df = pd.DataFrame(contacts)
    st.dataframe(df, use_container_width=True)
    
    # Delete Interface - simpler than dataframe selection for now
    st.subheader("Remove Connection")
    to_delete = st.selectbox("Select email to remove", [c['email'] for c in contacts])
    if st.button("Delete Selected"):
        data_manager.delete_contact(to_delete)
        st.success("Deleted.")
        st.rerun()

else:
    st.info("No contacts yet. Add one above!")
