import streamlit as st
import time
from backend.db_supabase import SupabaseManager

def run():
    # Modern Login Page CSS
    st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* HIDE STREAMLIT CHROME */
    [data-testid="stSidebar"] { display: none; }
    header, footer { visibility: hidden; }
    #MainMenu { display: none; }
    
    /* FULL VIEWPORT, NO SCROLL */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 50%, #ddd6fe 100%) !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 100vh;
    }
    
    /* Override dark theme for login */
    .stApp, .stApp * {
        color: #1e293b !important;
    }
    
    /* Form inputs */
    .stTextInput input {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        color: #1e293b !important;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }
    
    .stTextInput input::placeholder {
        color: #94a3b8 !important;
    }
    
    /* Buttons */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #f1f5f9 !important;
        border-radius: 12px !important;
        padding: 4px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        color: #64748b !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #1e293b !important;
    }
    
    /* Expander */
    .stExpander {
        background: transparent !important;
        border: none !important;
    }
    
    /* Container card styling */
    div[data-testid="stVerticalBlock"] > div[data-testid="element-container"]:has(.login-card-wrapper) {
        background: white;
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Floating animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .float-emoji {
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    .float-emoji:nth-child(2) { animation-delay: 0.5s; }
    .float-emoji:nth-child(3) { animation-delay: 1s; }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Layout
    col_hero, col_spacer, col_login = st.columns([1.2, 0.1, 1])
    
    # --- LEFT: HERO SECTION ---
    with col_hero:
        st.write("")
        st.write("")
        
        # Logo
        st.image("assets/logo.png", width=60)
        
        st.write("")
        
        # Headline
        st.markdown("""
        <h1 style="font-size: 3rem; font-weight: 800; color: #0f172a; line-height: 1.1; margin-bottom: 16px;">
            Learn Python.<br>
            <span style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Actually.
            </span>
        </h1>
        """, unsafe_allow_html=True)
        
        # Subtitle
        st.markdown("""
        <p style="font-size: 1.1rem; color: #475569; line-height: 1.6; max-width: 400px; margin-bottom: 24px;">
            Daily bite-sized lessons that actually stick.<br>
            Build real skills in just 15 minutes a day.
        </p>
        """, unsafe_allow_html=True)
        
        # Feature badges
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px;">
            <span style="background: white; padding: 8px 14px; border-radius: 50px; font-size: 0.85rem; font-weight: 500; color: #334155; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                📚 Daily Lessons
            </span>
            <span style="background: white; padding: 8px 14px; border-radius: 50px; font-size: 0.85rem; font-weight: 500; color: #334155; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                🎯 Active Recall
            </span>
            <span style="background: white; padding: 8px 14px; border-radius: 50px; font-size: 0.85rem; font-weight: 500; color: #334155; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                ⚡ AI Feedback
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Floating emojis
        st.markdown("""
        <div style="font-size: 2.5rem; margin-top: 20px;">
            <span class="float-emoji">🐍</span>
            <span class="float-emoji" style="margin-left: 20px;">💻</span>
            <span class="float-emoji" style="margin-left: 20px;">🚀</span>
        </div>
        """, unsafe_allow_html=True)
    
    # --- RIGHT: LOGIN CARD ---
    with col_login:
        st.write("")
        
        # Card container
        with st.container(border=True):
            st.markdown("""
            <h2 style="font-size: 1.4rem; font-weight: 700; color: #0f172a; margin-bottom: 4px;">
                Get Started
            </h2>
            <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 20px;">
                Start your Python journey today
            </p>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
            db = SupabaseManager()
            
            # --- SIGN IN TAB ---
            with tab1:
                with st.form("login_form"):
                    email = st.text_input("Email", placeholder="you@example.com")
                    password = st.text_input("Password", type="password", placeholder="Your password")
                    st.write("")
                    submit = st.form_submit_button("Sign In →", use_container_width=True)
                
                if submit:
                    if email and password:
                        with st.spinner("Signing in..."):
                            session = db.sign_in(email, password)
                            if session:
                                st.session_state["role"] = db.get_user_role(session.session.access_token)
                                st.session_state["auth_token"] = session.session.access_token
                                st.session_state["user_email"] = email
                                
                                try:
                                    import requests
                                    from utils import network
                                    ip = network.get_remote_ip()
                                    geo_info = {"ip": ip, "city": "Unknown", "country": "Unknown"}
                                    if ip:
                                        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=status,city,country", timeout=2)
                                        if resp.status_code == 200:
                                            data = resp.json()
                                            if data.get("status") == "success":
                                                geo_info["city"] = data.get("city")
                                                geo_info["country"] = data.get("country")
                                    ua = network.get_user_agent()
                                    db.log_activity(email, "LOGIN", {"role": st.session_state["role"], "geo": geo_info}, user_agent=ua)
                                except:
                                    db.log_activity(email, "LOGIN", {"role": st.session_state["role"]})
                                
                                st.rerun()
                            else:
                                st.error("Invalid email or password")
                    else:
                        st.warning("Please fill in all fields")
                
                # Forgot Password
                st.write("")
                with st.expander("🔑 Forgot password?"):
                    reset_email = st.text_input("Your email", key="reset_email", placeholder="you@example.com")
                    if st.button("Send Reset Link", key="reset_btn", use_container_width=True):
                        if reset_email and "@" in reset_email:
                            success, msg = db.reset_password(reset_email)
                            if success:
                                st.success("✅ Check your email!")
                            else:
                                st.error(msg)
                        else:
                            st.warning("Enter a valid email")
            
            # --- SIGN UP TAB ---
            with tab2:
                with st.form("signup_form"):
                    new_name = st.text_input("Name", placeholder="Your name")
                    new_email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
                    new_password = st.text_input("Password", type="password", placeholder="Min 6 characters", key="signup_pass")
                    st.write("")
                    submit_new = st.form_submit_button("Start Learning Free →", use_container_width=True)
                
                if submit_new:
                    if not new_name or not new_email or not new_password:
                        st.warning("Please fill in all fields")
                    elif len(new_password) < 6:
                        st.warning("Password must be at least 6 characters")
                    else:
                        with st.spinner("Creating account..."):
                            res = db.sign_up(new_email, new_password, new_name)
                            if res:
                                st.success("🎉 Check your email to confirm!")
                            else:
                                st.error("Sign up failed. Try a different email.")
            
            st.markdown("""
            <p style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 16px;">
                <span style="color: #10b981;">✓</span> Free forever · No credit card required
            </p>
            """, unsafe_allow_html=True)
