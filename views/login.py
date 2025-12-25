import streamlit as st
import time
from backend.db_supabase import SupabaseManager

def run():
    # 1. Custom CSS for Login Page (Watermark & Native Card)
    st.markdown("""
    <style>
    /* HIDE SIDEBAR on Login Page */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* BACKGROUND: Clean Light */
    .stApp {
        background-color: #FAFAFA !important;
        background-image: none !important;
    }
    
    /* GIANT WATERMARK TEXT */
    .stApp::before {
        content: "PYTHON TUTOR";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 13vw; 
        font-weight: 900;
        z-index: 0;
        white-space: nowrap;
        pointer-events: none;
        
        /* Gradient Text: Pink -> Blue -> Yellow */
        background: linear-gradient(135deg, #F9A8D4, #93C5FD, #FDE047); 
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        opacity: 0.12; 
        filter: blur(1px);
    }
    
    /* CARD STYLING: Applied to the Main Block Container directly */
    /* This avoids the "empty div" issue by styling the actual content wrapper */
    .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.8);
        
        padding: 3rem !important;
        max-width: 480px !important;
        
        /* Centering & Positioning */
        margin: auto !important;
        top: 8vh !important; /* Raise it up a bit (User Request) */
        position: relative;
    }
    
    /* HEADER INSIDE CARD */
    h2 {
        text-align: center;
        margin-bottom: 2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        color: #111827 !important;
    }
    
    /* TABS */
    div[data-baseweb="tab-list"] {
        background-color: transparent !important;
        margin-bottom: 1rem;
    }
    div[data-baseweb="tab-list"] p {
        color: #4B5563 !important; 
        font-weight: 600 !important;
    }
    
    /* BUTTONS */
    button[kind="primary"] {
        background-color: #2563EB !important;
        height: 48px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px -2px rgba(37, 99, 235, 0.4) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        margin-top: 10px !important;
    }
    button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
        transform: translateY(-1px);
    }
    
    /* Clean Input Fields */
    div[data-baseweb="input"] {
        border-radius: 8px !important;
        background-color: white !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

    # 2. Content (No more manual HTML wrappers)
    
    # Internal Header
    st.markdown("<h2>PyDaily</h2>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["Sign In", "New Account"]) # Renamed for clarity
    
    db = SupabaseManager()
    
    # --- LOGIN FORM ---
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="student@example.com")
            password = st.text_input("Password", type="password")
            
            submit = st.form_submit_button("Enter Classroom", type="primary", use_container_width=True)
        
        if submit:
            with st.spinner("Authenticating..."):
                session = db.sign_in(email, password)
                if session:
                    token = session.session.access_token
                    role = db.get_user_role(token)
                    st.session_state["role"] = role
                    st.session_state["auth_token"] = token
                    st.session_state["user_email"] = email
                    st.success("Welcome back!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Invalid credentials")


    # --- SIGN UP FORM ---
    with tab2:
        st.write("") # Spacer
        with st.form("signup_form"):
            new_email = st.text_input("Email")
            new_name = st.text_input("Full Name")
            new_password = st.text_input("Password", type="password")
            
            submit_new = st.form_submit_button("Join PyDaily", type="primary", use_container_width=True)
        
        if submit_new:
            if len(new_password) < 6:
                st.warning("Password min 6 chars")
            else:
                with st.spinner("Creating account..."):
                    res = db.sign_up(new_email, new_password, new_name)
                    if res:
                        st.success("Success! Please Sign In.")
                    else:
                        st.error("Error creating account.")
                        st.caption("⚠️ If you were manually enrolled by an Admin, you already have an account! Please ask for your initial password and use the **Sign In** tab.")
