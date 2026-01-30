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
    
    /* BACKGROUND & TYPOGRAPHY */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif !important;
        /* Force Single Page (No Scroll) */
        height: 100vh;
        overflow: hidden;
    }
    
    /* WATERMARK TEXT (Fixed Size) */
    .stApp::before {
        content: "PYTHON AI TUTOR";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 11vw; /* Reduced from 15vw to fit better */
        font-weight: 900;
        z-index: 0;
        white-space: nowrap;
        pointer-events: none;
        
        /* Subtle Gradient */
        background: linear-gradient(135deg, #E2E8F0, #F1F5F9); 
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        opacity: 0.4;
    }
    
    /* ANIMATIONS */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
    
    /* LOGO & HERO SECTION */
    .hero-container {
        padding-top: 5vh; /* Use VH for responsive vertical centering */
        z-index: 10;
        position: relative;
    }
    
    .hero-title {
        font-size: 3.5rem; /* Slightly smaller to prevent scroll */
        font-weight: 800;
        line-height: 1.1;
        /* Vibrant Gradient */
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.03em;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #475569;
        line-height: 1.5;
        margin-bottom: 2rem;
        font-weight: 400;
        max-width: 95%;
    }
    
    /* COMPACT FEATURE GRID (To fit in 100vh) */
    .feature-grid {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: white;
        padding: 0.6rem 0.9rem;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        font-weight: 600;
        color: #334155;
        font-size: 0.85rem;
    }
    
    /* LOGIN CARD (Right Column) */
    .login-container {
        margin-top: 15vh; /* Push down slightly but ensure it fits */
    }
    
    /* BUTTON STYLING (Vibrant) */
    button[kind="primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        border: none;
        height: 48px;
        font-weight: 700;
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        margin-top: 0.5rem;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4);
    }
    
    /* TABS */
    div[data-baseweb="tab-list"] {
        background-color: transparent !important;
        margin-bottom: 1rem;
    }
    
    /* Inputs */
    input {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
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
