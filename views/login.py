import streamlit as st
import time
from backend.db_supabase import SupabaseManager

def run():
    # 1. Custom CSS for Landing Page (Premium Design)
    st.markdown("""
    <style>
    /* IMPORT PREMIUM FONT: 'Outfit' */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* HIDE SIDEBAR & DECORATION */
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* FULL PAGE - NO SCROLL INITIALLY, BUT ALLOW IF CONTENT EXPANDS */
    html, body {
        height: 100vh !important;
        overflow-y: auto !important; /* Allow scroll if needed (expander) */
        scrollbar-width: none; /* Firefox */
    }
    
    /* Hide Scrollbar (Chrome/Safari) */
    html::-webkit-scrollbar, body::-webkit-scrollbar, .stApp::-webkit-scrollbar {
        display: none;
    }
    
    .stApp {
        background: linear-gradient(135deg, #faf5ff 0%, #ede9fe 50%, #ddd6fe 100%) !important;
        font-family: 'Outfit', sans-serif !important;
        min-height: 100vh !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    
    /* HERO SECTION */
    .hero-container {
        padding-top: 3vh;
        z-index: 10;
        position: relative;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
        letter-spacing: -0.03em;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        color: #475569;
        line-height: 1.5;
        margin-bottom: 1.2rem;
        font-weight: 400;
    }
    
    /* COMPACT FEATURE GRID */
    .feature-grid {
        display: flex;
        gap: 0.6rem;
        margin-bottom: 1rem;
    }
    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        background: white;
        padding: 0.5rem 0.8rem;
        border-radius: 50px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        font-weight: 500;
        color: #334155;
        font-size: 0.8rem;
    }
    
    /* LOGIN CARD */
    .login-container {
        margin-top: 5vh; /* Reduced top margin to give more room */
    }
    
    /* PILL TABS - 50/50 SPLIT */
    div[data-baseweb="tab-list"] {
        background: #f1f5f9 !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 0 !important;
        display: flex !important;
        width: 100% !important;
    }
    
    button[data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 10px !important;
        padding: 8px 0 !important;
        font-weight: 600 !important;
        color: #64748b !important;
        flex: 1 !important; /* Force 50% width */
        text-align: center !important;
        justify-content: center !important;
    }
    
    button[aria-selected="true"] {
        background: white !important;
        color: #0f172a !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* BUTTON STYLING */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        height: 44px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Inputs */
    input {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }
    
    /* Expander styling */
    .stExpander {
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. Main Layout (2 Columns) - Use 'large' gap
    col_left, col_right = st.columns([1.5, 1], gap="large")
    
    # --- LEFT COLUMN: BRANDING & PITCH ---
    with col_left:
        st.markdown('<div class="hero-container">', unsafe_allow_html=True)
        
        # LOGO
        st.image("assets/logo.png", width=100) 
        
        st.write("")
        # REMOVED: Beta Badge
        
        st.markdown('<h1 class="hero-title">Master Python in<br>15 Minutes a Day</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="hero-subtitle">The AI-powered automated challenge. Stop starting "courses" you never finish.<br><b>No burnout. Just consistency.</b></h2>', unsafe_allow_html=True)
        
        # COMPACT FEATURES (Revised Copy)
        st.markdown("""
        <div class="feature-grid">
            <div class="feature-item">📚 Daily Micro-Lessons</div>
            <div class="feature-item">💡 Instant AI Feedback</div>
        </div>
        <div class="feature-grid">
            <div class="feature-item">🎯 Active Recall Quizzes</div>
            <div class="feature-item">🚀 Career-Track Curriculum</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # End hero-container

    # --- RIGHT COLUMN: LOGIN/SIGNUP CARD ---
    with col_right:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Native Container with Border
        with st.container(border=True):
            st.subheader("Join the Challenge")
            
            tab1, tab2 = st.tabs(["Sign In", "Sign Up"]) 
            db = SupabaseManager()

            # LOGIN FORM
            with tab1:
                with st.form("login_form"):
                    email = st.text_input("Email", placeholder="you@example.com")
                    password = st.text_input("Password", type="password")
                    st.write("")
                    submit = st.form_submit_button("Sign In ->", type="primary", use_container_width=True)
                
                if submit:
                    with st.spinner("Authenticating..."):
                        session = db.sign_in(email, password)
                        if session:
                            st.session_state["role"] = db.get_user_role(session.session.access_token)
                            st.session_state["auth_token"] = session.session.access_token
                            st.session_state["user_email"] = email
                            
                            # --- ANALYTICS: LOG LOGIN + GEO ---
                            try:
                                import requests
                                from utils import network
                                
                                ip = network.get_remote_ip()
                                geo_info = {"ip": ip, "city": "Unknown", "country": "Unknown"}
                                
                                if ip:
                                    # Free Tier: 45 requests/minute. Fine for login.
                                    # Timeout essential to not block UI.
                                    resp = requests.get(f"http://ip-api.com/json/{ip}?fields=status,city,country", timeout=2)
                                    if resp.status_code == 200:
                                        data = resp.json()
                                        if data.get("status") == "success":
                                            geo_info["city"] = data.get("city")
                                            geo_info["country"] = data.get("country")
                                
                                # Fetch UA
                                ua = network.get_user_agent()
                            
                                db.log_activity(email, "LOGIN", {
                                    "role": st.session_state["role"],
                                    "geo": geo_info
                                }, user_agent=ua)
                            except Exception as e:
                                # Fallback if GEO fails -> Log basic login
                                print(f"Geo-Log Failed: {e}")
                                db.log_activity(email, "LOGIN", {"role": st.session_state["role"], "geo_error": str(e)})

                            st.rerun()
                        else:
                            st.error("Login failed.")
                
                # Forgot Password Section
                st.markdown("---")
                with st.expander("🔑 Forgot your password?"):
                    st.write("Enter your email and we'll send you a reset link.")
                    reset_email = st.text_input("Email address", key="reset_email", placeholder="you@example.com")
                    if st.button("Send Reset Link", use_container_width=True):
                        if reset_email and "@" in reset_email:
                            with st.spinner("Sending reset link..."):
                                success, msg = db.reset_password(reset_email)
                                if success:
                                    st.success("✅ Reset link sent! Check your email (including spam folder).")
                                else:
                                    st.error(f"❌ {msg}")
                        else:
                            st.warning("Please enter a valid email address.")

            # SIGNUP FORM
            with tab2:
                st.write("Create your free account.")
                with st.form("signup_form"):
                    new_name = st.text_input("Name", placeholder="Your Name")
                    new_email = st.text_input("Email")
                    new_password = st.text_input("Choose Password", type="password")
                    st.write("")
                    submit_new = st.form_submit_button("Join Class (Free)", type="primary", use_container_width=True)
                
                if submit_new:
                    if len(new_password) < 6:
                        st.warning("Password min 6 chars")
                    else:
                        with st.spinner("Creating account..."):
                            res = db.sign_up(new_email, new_password, new_name)
                            if res:
                                st.success("Check email to confirm.")
                            else:
                                st.error("Failed.")
        
        st.markdown('</div>', unsafe_allow_html=True)
