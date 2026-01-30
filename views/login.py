import streamlit as st
import time
from backend.db_supabase import SupabaseManager

def run():
    # Modern Login Page with Blue/Purple Accents (Matching Portal Theme)
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
        height: 100vh;
        overflow: hidden;
    }
    
    /* Remove default padding */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* MAIN CONTAINER */
    .login-page {
        display: flex;
        height: 100vh;
        width: 100%;
        align-items: center;
        justify-content: center;
        padding: 20px;
        box-sizing: border-box;
    }
    
    /* SPLIT LAYOUT */
    .login-wrapper {
        display: flex;
        width: 100%;
        max-width: 1100px;
        gap: 60px;
        align-items: center;
    }
    
    /* LEFT SIDE - HERO */
    .hero-side {
        flex: 1.2;
        position: relative;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 30px;
    }
    
    .logo-icon {
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .logo-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .hero-headline {
        font-size: 3.2rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
        margin-bottom: 20px;
    }
    
    .hero-headline span {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: #475569;
        line-height: 1.6;
        margin-bottom: 30px;
        max-width: 420px;
    }
    
    /* FLOATING DECORATIVE ELEMENTS */
    .floating-elements {
        position: absolute;
        top: -20px;
        right: -40px;
        width: 200px;
        height: 200px;
        pointer-events: none;
    }
    
    .float-icon {
        position: absolute;
        font-size: 2.5rem;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));
    }
    
    .float-icon:nth-child(1) { top: 0; left: 20px; animation-delay: 0s; }
    .float-icon:nth-child(2) { top: 60px; left: 120px; animation-delay: 0.5s; }
    .float-icon:nth-child(3) { top: 120px; left: 40px; animation-delay: 1s; }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-12px) rotate(5deg); }
    }
    
    /* FEATURE BADGES */
    .features {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }
    
    .feature-badge {
        background: white;
        padding: 10px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #334155;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* RIGHT SIDE - LOGIN CARD */
    .login-side {
        flex: 0.9;
    }
    
    .login-card {
        background: white;
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }
    
    .card-subtitle {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 24px;
    }
    
    /* STREAMLIT FORM OVERRIDES */
    .login-card input {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 1rem !important;
    }
    
    .login-card input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .login-card .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    
    .login-card .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3) !important;
    }
    
    .divider {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin: 16px 0;
    }
    
    .trust-badge {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 20px;
    }
    
    .trust-badge span {
        color: #10b981;
    }
    
    /* TABS OVERRIDE */
    .stTabs [data-baseweb="tab-list"] {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 4px;
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* MOBILE RESPONSIVE */
    @media (max-width: 768px) {
        .login-wrapper {
            flex-direction: column;
            gap: 30px;
        }
        .hero-headline { font-size: 2.2rem; }
        .floating-elements { display: none; }
        .login-card { padding: 24px; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Layout
    col_hero, col_login = st.columns([1.3, 1], gap="large")
    
    # --- LEFT: HERO SECTION ---
    with col_hero:
        st.markdown("""
        <div class="hero-side">
            <div class="logo">
                <div class="logo-icon">🐍</div>
                <div class="logo-text">PyDaily</div>
            </div>
            
            <h1 class="hero-headline">
                Learn Python.<br><span>Actually.</span>
            </h1>
            
            <p class="hero-subtitle">
                Daily bite-sized lessons that actually stick. Build real skills in just 15 minutes a day. No fluff, no burnout.
            </p>
            
            <div class="features">
                <div class="feature-badge">📚 Daily Lessons</div>
                <div class="feature-badge">🎯 Active Recall</div>
                <div class="feature-badge">⚡ AI Feedback</div>
            </div>
            
            <div class="floating-elements">
                <div class="float-icon">🐍</div>
                <div class="float-icon">💻</div>
                <div class="float-icon">🚀</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # --- RIGHT: LOGIN CARD ---
    with col_login:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Get Started</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Join thousands learning Python the smart way</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        db = SupabaseManager()
        
        # --- SIGN IN TAB ---
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com", label_visibility="collapsed")
                password = st.text_input("Password", type="password", placeholder="Your password", label_visibility="collapsed")
                submit = st.form_submit_button("Sign In →", use_container_width=True)
            
            if submit:
                if email and password:
                    with st.spinner("Signing in..."):
                        session = db.sign_in(email, password)
                        if session:
                            st.session_state["role"] = db.get_user_role(session.session.access_token)
                            st.session_state["auth_token"] = session.session.access_token
                            st.session_state["user_email"] = email
                            
                            # Analytics
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
            with st.expander("🔑 Forgot password?", expanded=False):
                reset_email = st.text_input("Enter your email", key="reset_email", placeholder="you@example.com", label_visibility="collapsed")
                if st.button("Send Reset Link", key="reset_btn"):
                    if reset_email and "@" in reset_email:
                        success, msg = db.reset_password(reset_email)
                        if success:
                            st.success("✅ Check your email for reset link!")
                        else:
                            st.error(msg)
                    else:
                        st.warning("Enter a valid email")
        
        # --- SIGN UP TAB ---
        with tab2:
            with st.form("signup_form"):
                new_name = st.text_input("Name", placeholder="Your name", label_visibility="collapsed")
                new_email = st.text_input("Email", placeholder="you@example.com", key="signup_email", label_visibility="collapsed")
                new_password = st.text_input("Password", type="password", placeholder="Choose a password (min 6 chars)", key="signup_pass", label_visibility="collapsed")
                submit_new = st.form_submit_button("Start Learning Free →", use_container_width=True)
            
            if submit_new:
                if not new_name or not new_email or not new_password:
                    st.warning("Please fill in all fields")
                elif len(new_password) < 6:
                    st.warning("Password must be at least 6 characters")
                else:
                    with st.spinner("Creating your account..."):
                        res = db.sign_up(new_email, new_password, new_name)
                        if res:
                            st.success("🎉 Check your email to confirm!")
                        else:
                            st.error("Sign up failed. Try a different email.")
        
        st.markdown('<div class="trust-badge"><span>✓</span> Free forever · No credit card required</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
