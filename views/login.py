import streamlit as st
from backend.db_supabase import SupabaseManager

def run():
    # ============================================
    # MODERN LOGIN PAGE - V3 DESIGN (Blue/Purple)
    # ============================================
    st.markdown("""
    <style>
    /* FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* HIDE STREAMLIT CHROME */
    [data-testid="stSidebar"], header, footer, #MainMenu { display: none !important; }
    
    /* NO SCROLL - FIXED VIEWPORT */
    html, body, .stApp {
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #faf5ff 0%, #ede9fe 40%, #ddd6fe 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* FORCE TEXT COLORS */
    h1, h2, h3, p, span, label, .stMarkdown { color: #1e293b !important; }
    
    /* ============ LAYOUT ============ */
    .main-wrapper {
        display: flex;
        width: 100%;
        max-width: 1000px;
        align-items: center;
        gap: 40px;
        padding: 20px;
    }
    
    .hero-section {
        flex: 1.1;
    }
    
    .login-section {
        flex: 0.9;
    }
    
    /* ============ HERO ============ */
    .logo-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 24px;
    }
    
    .logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
    }
    
    .logo-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.15;
        margin-bottom: 16px;
    }
    
    .hero-title .gradient {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        color: #64748b;
        line-height: 1.5;
        margin-bottom: 20px;
    }
    
    .badges {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    
    .badge {
        background: white;
        padding: 8px 14px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 500;
        color: #475569;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    }
    
    .illustration {
        margin-top: 10px;
    }
    
    .float-icons {
        display: flex;
        gap: 20px;
        font-size: 2rem;
    }
    
    .float-icons span {
        animation: bob 2.5s ease-in-out infinite;
    }
    .float-icons span:nth-child(2) { animation-delay: 0.4s; }
    .float-icons span:nth-child(3) { animation-delay: 0.8s; }
    
    @keyframes bob {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    /* ============ LOGIN CARD ============ */
    .login-card {
        background: white;
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    
    .card-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }
    
    .card-sub {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 20px;
    }
    
    /* CUSTOM PILL TABS - Override Streamlit */
    .stTabs [data-baseweb="tab-list"] {
        background: #f1f5f9 !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 0 !important;
        border: none !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        color: #64748b !important;
        border: none !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #3b82f6 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #0f172a !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"], 
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input {
        background: #f8fafc !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        font-size: 0.95rem !important;
        color: #1e293b !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
    }
    
    .stTextInput label { display: none !important; }
    
    /* BUTTONS */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(59,130,246,0.25) !important;
    }
    
    /* EXPANDER */
    .stExpander {
        border: none !important;
        background: transparent !important;
    }
    
    .stExpander summary {
        color: #3b82f6 !important;
        font-weight: 500 !important;
    }
    
    .trust-text {
        text-align: center;
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 16px;
    }
    
    .trust-text .check {
        color: #10b981;
    }
    
    /* MOBILE */
    @media (max-width: 768px) {
        .main-wrapper {
            flex-direction: column;
            padding: 16px;
            gap: 24px;
            overflow-y: auto;
            max-height: 100vh;
        }
        .hero-title { font-size: 2rem; }
        .login-card { padding: 24px; }
        .float-icons { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Layout
    col1, col2 = st.columns([1.2, 1], gap="medium")
    
    with col1:
        # Hero Section - All HTML for proper control
        st.markdown("""
        <div class="hero-section">
            <div class="logo-row">
                <div class="logo-icon">🐍</div>
                <div class="logo-name">PyDaily</div>
            </div>
            
            <h1 class="hero-title">
                Learn Python.<br>
                <span class="gradient">Actually.</span>
            </h1>
            
            <p class="hero-subtitle">
                Daily bite-sized lessons that actually stick.<br>
                Build real skills in just 15 min/day.
            </p>
            
            <div class="badges">
                <span class="badge">📚 Daily Lessons</span>
                <span class="badge">🎯 Active Recall</span>
                <span class="badge">⚡ AI Feedback</span>
            </div>
            
            <div class="float-icons">
                <span>🐍</span>
                <span>💻</span>
                <span>🎯</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Login Card
        st.markdown("""
        <div class="login-card">
            <div class="card-header">Get Started</div>
            <div class="card-sub">Start your Python journey today</div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        db = SupabaseManager()
        
        with tab1:
            email = st.text_input("Email", placeholder="you@example.com", key="login_email", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", key="login_pass", label_visibility="collapsed")
            
            if st.button("Sign In →", key="login_btn", use_container_width=True):
                if email and password:
                    with st.spinner(""):
                        session = db.sign_in(email, password)
                        if session:
                            st.session_state["role"] = db.get_user_role(session.session.access_token)
                            st.session_state["auth_token"] = session.session.access_token
                            st.session_state["user_email"] = email
                            try:
                                import requests
                                from utils import network
                                ip = network.get_remote_ip()
                                geo = {"ip": ip, "city": "Unknown", "country": "Unknown"}
                                if ip:
                                    r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,city,country", timeout=2)
                                    if r.ok and r.json().get("status") == "success":
                                        geo.update(r.json())
                                db.log_activity(email, "LOGIN", {"role": st.session_state["role"], "geo": geo}, user_agent=network.get_user_agent())
                            except:
                                db.log_activity(email, "LOGIN", {"role": st.session_state["role"]})
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                else:
                    st.warning("Fill in all fields")
            
            with st.expander("🔑 Forgot password?"):
                reset_email = st.text_input("", placeholder="Your email", key="reset_email", label_visibility="collapsed")
                if st.button("Send Reset Link", key="reset_btn"):
                    if reset_email and "@" in reset_email:
                        ok, msg = db.reset_password(reset_email)
                        st.success("✅ Check your email!") if ok else st.error(msg)
                    else:
                        st.warning("Enter valid email")
        
        with tab2:
            new_name = st.text_input("", placeholder="Your name", key="name", label_visibility="collapsed")
            new_email = st.text_input("", placeholder="Email", key="new_email", label_visibility="collapsed")
            new_pass = st.text_input("", placeholder="Password (min 6 chars)", type="password", key="new_pass", label_visibility="collapsed")
            
            if st.button("Start Learning Free →", key="signup_btn", use_container_width=True):
                if new_name and new_email and new_pass:
                    if len(new_pass) < 6:
                        st.warning("Password too short")
                    else:
                        res = db.sign_up(new_email, new_pass, new_name)
                        st.success("🎉 Check email to confirm!") if res else st.error("Signup failed")
                else:
                    st.warning("Fill in all fields")
        
        st.markdown('<p class="trust-text"><span class="check">✓</span> Free forever · No credit card</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
