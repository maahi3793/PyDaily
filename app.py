import streamlit as st

# 1. Global Config (Must be first)
st.set_page_config(page_title="PyDaily Platform", page_icon="🐍", layout="wide")

# 2. Session State Initialization
if "role" not in st.session_state:
    st.session_state["role"] = "guest" 

# 3. Router Logic
def main():
    role = st.session_state["role"]
    
    # --- LOGOUT BUTTON (Global) ---
    if role != "guest":
        with st.sidebar:
            if st.button("Logout", type="secondary"):
                st.session_state["role"] = "guest"
                st.session_state.pop("user_email", None)
                st.rerun()

    # --- ROUTING ---
    if role == "guest":
        from views import login
        login.run()
        
    elif role == "admin":
        from views.admin import dashboard
        dashboard.run()
        
    elif role == "student" or role == "user":
        # 'user' is the new standard role for students
        # st.info("🎓 Student Portal Under Construction")
        from views.student import dashboard
        dashboard.run()
        
    else:
        st.error(f"Unknown Role: {role}")
        if st.button("Reset"):
            st.session_state["role"] = "guest"
            st.rerun()

if __name__ == "__main__":
    main()
