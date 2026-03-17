import streamlit as st
import time
from backend.db_supabase import SupabaseManager

def run():
    # 1. Custom CSS for Landing Page (Premium Design - Zen Nature)
    st.markdown("""
    <style>
    /* IMPORT PREMIUM FONTS */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');
    
    /* FORCE LIGHT MODE */
    .stApp, .stApp * {
        color-scheme: light !important;
    }
    
    /* Zen Nature Variables */
    :root {
        --bg-beige: #f9f6f0;
        --sage-green: #8aa899;
        --sage-dark: #6a8879;
        --sage-light: #e6ece9;
        --text-main: #2c3e35;
        --text-muted: #5a7065;
        --border-light: #dce3df;
    }
    
    /* Typography Overrides */
    .stApp p, .stApp span:not(.logo-icon), .stApp label, .stApp div, .stApp li {
        color: var(--text-main) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* HIDE SIDEBAR & DECORATION */
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* FULL PAGE BACKGROUND */
    .stApp {
        background-color: var(--bg-beige) !important;
        background-image: 
            radial-gradient(circle at 100% 0%, var(--sage-light) 0%, transparent 40%),
            radial-gradient(circle at 0% 100%, #f4eee2 0%, transparent 40%) !important;
        font-family: 'DM Sans', sans-serif !important;
        min-height: 100vh !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }
    
    /* HERO SECTION */
    .hero-container {
        padding-top: 3vh;
        z-index: 10;
        position: relative;
    }
    
    .hero-title {
        font-family: 'DM Serif Display', serif !important;
        font-size: 3.5rem;
        font-weight: 400;
        line-height: 1.1;
        color: var(--text-main) !important;
        margin-bottom: 0.8rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-muted) !important;
        line-height: 1.6;
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
        background: rgba(255, 255, 255, 0.6);
        padding: 0.5rem 0.8rem;
        border-radius: 100px;
        border: 1px solid var(--border-light);
        font-weight: 500;
        color: var(--text-main);
        font-size: 0.85rem;
    }
    
    /* LOGIN CARD CONTAINER */
    .login-container {
        margin-top: 5vh; 
    }
    
    /* Streamlit Container (The Form Card) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 32px !important;
        border: none !important;
        background: white !important;
        box-shadow: 0 12px 40px rgba(44, 62, 53, 0.08) !important;
        padding: 10px !important;
    }
    
    /* PILL TABS - 50/50 SPLIT */
    div[data-baseweb="tab-list"] {
        background: #f0ede5 !important;
        border-radius: 100px !important;
        padding: 4px !important;
        gap: 0 !important;
        display: flex !important;
        width: 100% !important;
    }
    
    button[data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 100px !important;
        padding: 8px 0 !important;
        font-weight: 500 !important;
        color: var(--text-muted) !important;
        flex: 1 !important;
        text-align: center !important;
        justify-content: center !important;
    }
    
    button[aria-selected="true"] {
        background: white !important;
        color: var(--text-main) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    
    div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* BUTTON STYLING */
    .stButton > button, .stFormSubmitButton > button {
        background: var(--sage-dark) !important;
        color: white !important;
        border: none !important;
        height: 48px !important;
        font-weight: 500 !important;
        border-radius: 100px !important;
        font-size: 1rem !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: #557061 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(106, 136, 121, 0.25) !important;
    }
    
    /* Button Secondary (For Explore Demo) */
    .stButton[data-testid="stButton"] button:has(div:contains("Explore Demo")) {
        background: transparent !important;
        border: 1px solid var(--sage-dark) !important;
        color: var(--sage-dark) !important;
        box-shadow: none !important;
    }
    .stButton[data-testid="stButton"] button:has(div:contains("Explore Demo")):hover {
        background: var(--sage-light) !important;
    }
    
    /* Inputs */
    input {
        background-color: var(--bg-beige) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 100px !important;
        color: var(--text-main) !important;
        padding-left: 1rem !important;
    }
    input:focus {
        border-color: var(--sage-green) !important;
        background: white !important;
        box-shadow: 0 0 0 4px var(--sage-light) !important;
    }
    
    /* Expander styling */
    .stExpander {
        border: none !important;
        background: transparent !important;
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
        
        st.markdown('<h1 class="hero-title">Grow 1% Better<br>Every Day.</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="hero-subtitle">The consistent, peaceful path to Python mastery. Build the daily habit of coding—without the burnout.</h2>', unsafe_allow_html=True)
        
        # COMPACT FEATURES (Zen Copy)
        st.markdown("""
        <div class="feature-grid">
            <div class="feature-item">🌱 Bite-sized Lessons</div>
            <div class="feature-item">☕ Streak & Consistency</div>
        </div>
        <div class="feature-grid">
            <div class="feature-item">🧠 Smart Review</div>
            <div class="feature-item">🗻 Career Growth</div>
        </div>
        """, unsafe_allow_html=True)
        
        # --- DEMO BUTTON (Left Column) ---
        st.write("")
        if st.button("🎮 Try Free Demo — No Signup Required", use_container_width=True, key="demo_btn_left"):
            st.session_state["role"] = "demo"
            st.rerun()
        st.caption("See real lessons, take a quiz, explore the dashboard.")
        
        # --- GMAIL PHONE MOCKUP ---
        st.write("")
        st.markdown("""
        <div style="max-width: 280px; margin: 0 auto;">
            <!-- Phone Frame -->
            <div style="background: #2c3e35; border-radius: 30px; padding: 10px; box-shadow: 0 20px 60px rgba(44, 62, 53, 0.12);">
                <!-- Status Bar -->
                <div style="text-align: center; color: #8aa899; font-size: 11px; padding: 6px 0 4px;">
                    9:41 AM
                </div>
                <!-- Gmail Header -->
                <div style="background: #ffffff; border-radius: 20px 20px 0 0; padding: 12px 15px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.3rem;">📧</span>
                        <span style="font-weight: 700; font-size: 1.1rem; color: #2c3e35;">Inbox</span>
                        <span style="margin-left: auto; background: #e07a5f; color: white; border-radius: 10px; padding: 1px 7px; font-size: 11px; font-weight: 600;">3 new</span>
                    </div>
                </div>
                <!-- Email List -->
                <div style="background: #ffffff; padding: 0;">
                    <!-- Email 1 -->
                    <div style="padding: 12px 15px; border-bottom: 1px solid #dce3df; background: #fdfyf9;">
                        <div style="font-weight: 700; font-size: 0.85rem; color: #2c3e35;">PyDaily</div>
                        <div style="font-size: 0.82rem; color: #2c3e35; font-weight: 600;">🐍 Day 1: Variables & Data Types</div>
                        <div style="font-size: 0.75rem; color: #5a7065; margin-top: 2px;">Welcome to your Python journey! Today we...</div>
                    </div>
                    <!-- Email 2 -->
                    <div style="padding: 12px 15px; border-bottom: 1px solid #dce3df; background: #eef6ff;">
                        <div style="font-weight: 700; font-size: 0.85rem; color: #2c3e35;">PyDaily</div>
                        <div style="font-size: 0.82rem; color: #2c3e35; font-weight: 600;">⚡ Mid-Day Boost: Keep Going!</div>
                        <div style="font-size: 0.75rem; color: #5a7065; margin-top: 2px;">"The expert was once a beginner" — here's your...</div>
                    </div>
                    <!-- Email 3 -->
                    <div style="padding: 12px 15px; background: #eef6ff;">
                        <div style="font-weight: 700; font-size: 0.85rem; color: #2c3e35;">PyDaily</div>
                        <div style="font-size: 0.82rem; color: #2c3e35; font-weight: 600;">🌙 Nightly Check-in: Day 1</div>
                        <div style="font-size: 0.75rem; color: #5a7065; margin-top: 2px;">Did you finish the challenge? Tomorrow we'll...</div>
                    </div>
                </div>
                <!-- Bottom Nav -->
                <div style="background: #ffffff; border-radius: 0 0 20px 20px; padding: 8px; text-align: center;">
                    <span style="font-size: 0.7rem; color: #8aa899;">📩 Mail &nbsp;&nbsp; 💬 Chat &nbsp;&nbsp; 📹 Meet</span>
                </div>
            </div>
        </div>
        <p style="text-align: center; color: #5a7065; font-size: 0.8rem; margin-top: 10px;">↑ Your inbox as a PyDaily student</p>
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
                    submit = st.form_submit_button("Sign In 🌿", type="primary", use_container_width=True)
                
                if submit:
                    with st.spinner("Authenticating..."):
                        session = db.sign_in(email, password)
                        if session:
                            st.session_state["role"] = db.get_user_role(session.session.access_token)
                            st.session_state["auth_token"] = session.session.access_token
                            st.session_state["user_email"] = email
                            
                            # === SAVE TO COOKIES FOR PERSISTENT LOGIN ===
                            try:
                                from streamlit_app import save_auth_cookies
                                save_auth_cookies(session.session.access_token, session.session.refresh_token, email)
                            except Exception as cookie_err:
                                print(f"⚠️ Cookie save failed: {cookie_err}")
                            

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
                    submit_new = st.form_submit_button("Join Class (Free) 🌿", type="primary", use_container_width=True)
                
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
        
        # --- DEMO BUTTON (Below Signup) ---
        st.divider()
        st.caption("Not ready to sign up yet?")
        if st.button("🎮 Explore Demo Instead", use_container_width=True, key="demo_btn_right"):
            st.session_state["role"] = "demo"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
