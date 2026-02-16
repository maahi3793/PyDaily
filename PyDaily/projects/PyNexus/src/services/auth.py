import os
from supabase import create_client, Client
from dotenv import load_dotenv

import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Running in a bundle
    base_path = Path(sys._MEIPASS)
else:
    # Running in normal Python environment
    base_path = Path(__file__).parent.parent.parent

env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

class AuthService:
    def __init__(self):
        print("DEBUG: AuthService initializing...")
        url = os.environ.get("SUPABASE_URL")
        # Try Service Key first (Admin), then fall back to Anon Key
        key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_KEY")
        print(f"DEBUG: Supabase URL: {url}")
        print(f"DEBUG: Supabase Key found: {'Yes' if key else 'No'}")
        
        if not url or not key:
            print("Warning: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")
            self.client = None
        else:
            try:
                print("DEBUG: Creating Supabase client...")
                self.client: Client = create_client(url, key)
                print("DEBUG: Supabase client created successfully.")
            except Exception as e:
                print(f"DEBUG: Failed to create Supabase client: {e}")
                self.client = None

    def login(self, email, password):
        if not self.client:
            raise Exception("Supabase client not initialized. Check .env file.")
        return self.client.auth.sign_in_with_password({"email": email, "password": password})
    
    def set_session(self, access_token, refresh_token=None):
        """Manually sets the session for the client using a stored token."""
        if not self.client: return
        try:
             # If refresh token is missing, we might only be able to set session for current request
             # But supabase-py usually wants both or just access token?
             # set_session(access_token, refresh_token)
             if refresh_token:
                 self.client.auth.set_session(access_token, refresh_token)
             else:
                 # Logic to set header or minimal session?
                 # Actually, get_user(token) is better if we just want user.
                 pass
        except Exception as e:
            print(f"DEBUG: Failed to set session: {e}")

    def get_user_from_token(self, token):
        """Gets user object using a jwt token."""
        if not self.client: return None
        try:
            return self.client.auth.get_user(token)
        except Exception as e:
            print(f"DEBUG: Get User from Token Failed: {e}")
            return None

    def get_user(self):
        if not self.client:
            return None
        return self.client.auth.get_user()

    def get_user_role(self, user_id):
        """Fetches role from profiles table."""
        if not self.client: return "student"
        try:
            res = self.client.table('profiles').select('role').eq('id', user_id).single().execute()
            return res.data.get('role', 'student') if res.data else "student"
        except Exception as e:
            print(f"DEBUG: Role Fetch Failed: {e}")
            return "student"

    def get_user_profile(self, user_id):
        """Fetches full profile metrics (name, role, etc) from profiles table."""
        if not self.client: return {}
        try:
            res = self.client.table('profiles').select('*').eq('id', user_id).single().execute()
            return res.data if res.data else {}
        except Exception as e:
            print(f"DEBUG: Profile Fetch Failed: {e}")
            return {}
