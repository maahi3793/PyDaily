import os
import sys

# Ensure working directory is always this script's folder (PyDaily/)
# This fixes Streamlit Cloud which runs from repo root, not PyDaily/
_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_script_dir)
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta

# 1. Global Config (Must be first)
st.set_page_config(
    page_title="PyDaily: The 15-Minute Python Challenge", 
    page_icon="assets/logo.png", 
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Cookie Manager (for persistent sessions)
# Note: CookieManager uses Streamlit widgets internally, so we store it in session_state instead of caching
def get_cookie_manager():
    if "cookie_manager" not in st.session_state:
        st.session_state["cookie_manager"] = stx.CookieManager()
    return st.session_state["cookie_manager"]

cookie_manager = get_cookie_manager()

# 3. Session Persistence Logic
def restore_session_from_cookie():
    """Check if we have a saved auth token in cookies and restore session."""
    if st.session_state.get("role") != "guest":
        return  # Already logged in
    
    saved_token = cookie_manager.get("pydaily_auth_token")
    saved_refresh = cookie_manager.get("pydaily_refresh_token")
    saved_email = cookie_manager.get("pydaily_user_email")
    
    if saved_token and saved_email:
        # Validate the token is still valid
        try:
            from backend.db_supabase import SupabaseManager
            db = SupabaseManager()
            
            # 1. Try with existing access token
            user = db.supabase.auth.get_user(saved_token)
            
            if user and user.user:
                # Token is valid - restore session
                role = db.get_user_role(saved_token)
                st.session_state["role"] = role
                st.session_state["auth_token"] = saved_token
                st.session_state["user_email"] = saved_email
                print(f"🔓 Session restored from cookie for {saved_email}")
                return True
            else:
                raise Exception("Access Token Invalid")

        except Exception as e:
            # 2. Access Token Expired/Invalid -> Try Refresh Token
            if saved_refresh:
                print(f"🔄 Access token expired. Attempting refresh...")
                try:
                    res = db.refresh_session(saved_refresh)
                    if res and res.session:
                        new_access = res.session.access_token
                        new_refresh = res.session.refresh_token
                        
                        # Update Session State
                        role = db.get_user_role(new_access)
                        st.session_state["role"] = role
                        st.session_state["auth_token"] = new_access
                        st.session_state["user_email"] = saved_email
                        
                        # Update Cookies (Rotate Tokens)
                        save_auth_cookies(new_access, new_refresh, saved_email)
                        print(f"✅ Session Refreshed & Restored for {saved_email}")
                        return True
                except Exception as refresh_err:
                     print(f"❌ Auto-Refresh Failed: {refresh_err}")
            
            # Token expired and refresh failed - clear cookies
            print(f"⚠️ Cookie session invalid/expired: {e}")
            clear_auth_cookies()
    
    return False

def save_auth_cookies(access_token, refresh_token, email, days=30):
    """Save auth token AND refresh token to browser cookies for persistence."""
    expiry = datetime.now() + timedelta(days=days)
    cookie_manager.set("pydaily_auth_token", access_token, expires_at=expiry, key="set_auth")
    cookie_manager.set("pydaily_refresh_token", refresh_token, expires_at=expiry, key="set_refresh")
    cookie_manager.set("pydaily_user_email", email, expires_at=expiry, key="set_email")
    print(f"🍪 Auth cookies saved for {email} (expires: {expiry})")

def clear_auth_cookies():
    """Clear auth cookies on logout."""
    cookies_to_clear = ["pydaily_auth_token", "pydaily_refresh_token", "pydaily_user_email"]
    
    for c in cookies_to_clear:
        if cookie_manager.get(c):
            cookie_manager.delete(c, key=f"del_{c}")
            
    print("🗑️ Auth cookies cleared")

# 4. Session State Initialization
if "role" not in st.session_state:
    st.session_state["role"] = "guest" 

# 5. Try to restore session from cookies (runs once per app load)
if "session_restored" not in st.session_state:
    restore_session_from_cookie()
    st.session_state["session_restored"] = True

# 6. Router Logic
def main():
    role = st.session_state["role"]
    
    # --- LOGOUT BUTTON (Restored for Gold Standard) ---
    if role != "guest":
        with st.sidebar:
            st.divider()
            # Subtle Logout
            if st.button("Logout"):
                from backend.db_supabase import SupabaseManager
                db = SupabaseManager()
                db.sign_out()
                
                # Clear both session state AND cookies
                st.session_state["role"] = "guest"
                st.session_state.pop("user_email", None)
                st.session_state.pop("auth_token", None)
                st.session_state.pop("session_restored", None)
                clear_auth_cookies()
                st.rerun()

    # --- ROUTING ---
    # 0. Public Routes (Query Param Based)
    query_params = st.query_params
    if query_params.get("page") == "unsubscribe":
        from views import unsubscribe
        unsubscribe.run()
        return # Stop execution of main app

    # 1. Private Routes (Role Based)
    if role == "guest":
        from views import login
        login.run()
    else:
        # PAUSE SCREEN FOR ALL LOGGED IN USERS
        st.markdown("""
        <div style="text-align: center; padding: 50px; margin-top: 50px; border: 1px solid #e0e0e0; border-radius: 12px; background-color: #f9fafb;">
            <h1 style="font-size: 2.5rem; color: #4F46E5; margin-bottom: 20px;">Dashboard is Paused</h1>
            <p style="font-size: 18px; color: #475569; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                Thank you for logging in! The student portal is temporarily paused for maintenance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout"):
            from backend.db_supabase import SupabaseManager
            db = SupabaseManager()
            db.sign_out()
            st.session_state["role"] = "guest"
            st.session_state.pop("user_email", None)
            st.session_state.pop("auth_token", None)
            st.session_state.pop("session_restored", None)
            clear_auth_cookies()
            st.rerun()

if __name__ == "__main__":
    main()
