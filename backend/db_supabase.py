from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

class SupabaseManager:
    """
    Gold Standard Supabase Manager
    - Handles strict Authenticated Calls (using Token)
    - Fetches Roles from 'profiles' table via RLS
    """
    
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            print("❌ Supabase Credentials Missing")
            self.supabase = None
            self.admin_supabase = None
        else:
            self.supabase: Client = create_client(url, key)
            
            # Initialize Admin Client if Service Key exists
            if service_key:
                self.admin_supabase: Client = create_client(url, service_key)
            else:
                self.admin_supabase = None

    # --- 1. AUTHENTICATION (The Gatekeeper) ---

    def sign_in(self, email, password):
        """Standard Auth Sign In"""
        if not self.supabase: return None
        try:
            res = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return res
        except Exception as e:
            print(f"Login Failed: {e}")
            return None

    def sign_up(self, email, password, full_name):
        """Standard Auth Sign Up (Trigger handles Profile creation)"""
        if not self.supabase:
            print("❌ Supabase Client is None")
            return None
            
        print(f"🔄 Attempting Signup for: {email}")
        try:
            res = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": { "full_name": full_name } # Passed to Trigger
                }
            })
            print(f"✅ Signup Result: {res}")
            return res
        except Exception as e:
            print(f"❌ Signup Failed Exception: {type(e).__name__}")
            print(f"❌ Error Details: {str(e)}")
            # Try to print response body if available
            if hasattr(e, 'message'): print(f"❌ Message: {e.message}")
            if hasattr(e, 'code'): print(f"❌ Code: {e.code}")
            return None

    def sign_out(self):
        """Sign Out"""
        if not self.supabase: return
        try:
            self.supabase.auth.sign_out()
        except:
            pass

    # --- 2. AUTHORIZATION (The Guard) ---

    def get_user_role(self, token):
        """
        Fetches the Role ('admin' or 'student') for a given Token.
        Uses RLS-protected 'profiles' table.
        """
        if not self.supabase or not token: return "guest"
        
        try:
            # 1. Provide Context (RLS needs this token)
            self.supabase.postgrest.auth(token)
            
            # 2. Get User ID from Token
            user = self.supabase.auth.get_user(token)
            if not user: return "guest"
            
            user_id = user.user.id
            
            # 3. Query 'profiles' logic
            # RLS ensures user can only read their own row (or Admin reads all)
            response = self.supabase.table('profiles').select('role').eq('id', user_id).single().execute()
            
            if response.data:
                return response.data.get('role', 'student')
            
            return "student" # Default fallback
            
        except Exception as e:
            print(f"Role Fetch Error: {e}")
            return "student" # Fail safe

    def get_user_profile(self, token):
        """
        Fetches full profile (Name, Role, etc.) AND Student Data (Day, Status)
        """
        if not self.supabase or not token: return None
        try:
            self.supabase.postgrest.auth(token)
            user = self.supabase.auth.get_user(token)
            if not user:
                print("❌ Auth User Not Found")
                return None
            
            # Debug: Print User ID
            print(f"👤 Fetching Profile for User ID: {user.user.id}")
            
            # Join with student_data
            # Note: We select *, student_data(*) to get everything
            response = self.supabase.table('profiles').select('*, student_data(current_day, status)').eq('id', user.user.id).single().execute()
            print(f"✅ Profile Found: {response.data}")
            
            # Flatten the structure for easier usage in UI
            data = response.data
            s_data = data.get('student_data', {})
            # Handle potential list/dict mismatch
            if isinstance(s_data, list) and s_data: s_data = s_data[0]
            elif not isinstance(s_data, dict): s_data = {}
            
            data['current_day'] = s_data.get('current_day', 1)
            data['status'] = s_data.get('status', 'pending')
            
            return data
        except Exception as e:
            print(f"❌ Profile Fetch Error: {type(e).__name__}")
            print(f"❌ Details: {str(e)}")
            if hasattr(e, 'code'): print(f"❌ DB Code: {e.code}")
            if hasattr(e, 'message'): print(f"❌ DB Message: {e.message}")
            return None

    def reset_password(self, email):
        """
        Sends a Password Reset Email (Magic Link)
        """
        if not self.supabase: return False, "Client Error"
        try:
            # redirect_to ensures they land on the app.
            print(f"🔄 Sending Reset Link to {email}...")
            self.supabase.auth.reset_password_email(email, options={'redirect_to': 'https://pydaily.streamlit.app/'})
            return True, "Check your email for the reset link."
        except Exception as e:
            print(f"❌ Reset Failed: {type(e).__name__}")
            print(f"❌ Error Details: {str(e)}")
            
            msg = str(e)
            if hasattr(e, 'message'): msg = e.message
            if hasattr(e, 'code'): 
                print(f"❌ Error Code: {e.code}")
                if e.code == 429:
                    msg = "Too many requests. Please wait a moment."
            
            return False, msg

    def admin_update_password(self, email, new_password):
        """
        ADMIN ONLY: Forcibly updates a user's password using Service Role.
        Finds user by Email first.
        """
        if not self.admin_supabase:
            return False, "Service Key missing in .env"
            
        try:
            print(f"👮 Admin fetching ID for {email}...")
            # 1. Find User ID
            # Note: list_users returns a UserList object, which we iterate
            page = self.admin_supabase.auth.admin.list_users()
            user_id = None
            for u in page:
                if u.email == email:
                    user_id = u.id
                    break
            
            if not user_id:
                return False, "User not found in Auth system."

            # 2. Update
            print(f"👮 Admin updating password for {user_id}...")
            r = self.admin_supabase.auth.admin.update_user_by_id(
                user_id, 
                {"password": new_password}
            )
            return True, "Password updated successfully!"
        except Exception as e:
            print(f"❌ Admin Update Failed: {e}")
            return False, str(e)

    # --- 3. STUDENT MANAGEMENT (Migration Support) ---

    def admin_get_all_students(self):
        """
        Fetches all profiles with role 'student' and their progress.
        """
        if not self.admin_supabase: return []
        try:
            # Join profiles with student_data with proper error handling
            res = self.admin_supabase.table('profiles').select('email, full_name, role, student_data(current_day, status)').eq('role', 'student').execute()
            
            students = []
            for row in res.data:
                s_data = row.get('student_data')
                # Handle list vs dict return
                if isinstance(s_data, list) and s_data: s_data = s_data[0]
                elif not isinstance(s_data, dict): s_data = {}
                
                students.append({
                    "name": row.get('full_name', 'Unknown'),
                    "email": row.get('email'),
                    "day": s_data.get('current_day', 1),
                    "status": s_data.get('status', 'pending')
                })
            return students
        except Exception as e:
            print(f"❌ Fetch Students Failed: {e}")
            return []

    def admin_create_student(self, email, name, password="ChangeMe123!"):
        """
        Creates a new Auth User + Profile + Student Data row.
        """
        if not self.admin_supabase: return False, "No Admin Key"
        try:
            # 1. Create Auth User
            res = self.admin_supabase.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True,
                "user_metadata": { "full_name": name }
            })
            
            user_id = res.user.id
            
            # 2. Upsert student_data
            self.admin_supabase.table('student_data').upsert({
                "student_id": user_id,
                "current_day": 1,
                "status": "pending"
            }).execute()
            
            return True, "User Created"
        except Exception as e:
            msg = str(e)
            if "already registered" in msg:
                return False, "User already exists"
            print(f"❌ Create Student Failed: {e}")
            return False, msg

    def admin_update_student_progress(self, email, day=None, status=None):
        """
        Updates student_data for a given email.
        """
        if not self.admin_supabase: return False, "No Admin Key"
        
        user_id = self.admin_get_user_id(email)
        if not user_id: return False, f"User ID not found for {email}"
        
        try:
            payload = {}
            if day is not None: payload['current_day'] = day
            if status is not None: payload['status'] = status
            
            if payload:
                res = self.admin_supabase.table('student_data').update(payload).eq('student_id', user_id).execute()
                print(f"✅ DB Update Result: {res}")
                return True, "Updated"
            return True, "No Change"
        except Exception as e:
            print(f"❌ Update Progress Error: {e}")
            return False, str(e)

    def admin_delete_student(self, email):
        """
        Deletes a student (Auth User) + Cascades to Profile/Data if configured, 
        or we manually clean.
        """
        if not self.admin_supabase: return False
        
        user_id = self.admin_get_user_id(email)
        if not user_id: return False
        
        try:
            self.admin_supabase.auth.admin.delete_user(user_id)
            return True
        except Exception as e:
            print(f"Delete Error: {e}")
            return False

    def admin_get_user_id(self, email):
        """Helper to find UUID by Email"""
        if not self.admin_supabase: return None
        try:
            # Helper logic duplicated for safety/completeness if not strictly DRY
            page = self.admin_supabase.auth.admin.list_users()
            for u in page:
                if u.email == email: return u.id
            return None
        except: return None

    # --- 4. ANALYTICS (Insights) ---

    def save_quiz_result(self, token, day, score, total, answers):
        """
        Saves a student's quiz result to 'quiz_results'.
        Uses token for RLS.
        """
        if not self.supabase or not token: return False, "Auth Required"
        try:
            self.supabase.postgrest.auth(token)
            user = self.supabase.auth.get_user(token)
            if not user: return False, "User not found"
            
            # Using 'upsert' to ensure only the LATEST result is kept per day
            data = {
                "student_id": user.user.id,
                "day": day,
                "score": score,
                "total_questions": total,
                "answers_json": answers
            }
            
            # on_conflict ensures we update if (student_id, day) exists
            res = self.supabase.table('quiz_results').upsert(data, on_conflict='student_id, day').execute()
            print(f"✅ Quiz Saved (Upsert): {res}")
            return True, "Saved"
        except Exception as e:
            print(f"❌ Save Quiz Failed: {e}")
            return False, str(e)

    def admin_get_quiz_results(self, day_filter=None):
        """
        ADMIN: Fetches ALL quiz results for analysis.
        """
        if not self.admin_supabase: return []
        try:
            query = self.admin_supabase.table('quiz_results').select('*')
            if day_filter:
                query = query.eq('day', day_filter)
                
            res = query.execute()
            return res.data
        except Exception as e:
            print(f"❌ Admin Fetch Quiz Failed: {e}")
            return []

    def admin_get_pending_feedback_results(self):
        """
        ADMIN: Fetches quiz results that haven't received specific feedback emails yet.
        """
        if not self.admin_supabase: return []
        try:
            # We also join with user data if possible, but keep it simple for now (email fetched separately or via join)
            # Actually, to send email we need the student email.
            # Supabase doesn't easily join auth.users.
            # We will fetch results, then fetch user emails in batch or one-by-one?
            # Better: Let's assume we fetch results, and the caller resolves emails.
            res = self.admin_supabase.table('quiz_results').select('*').eq('feedback_sent', False).execute()
            return res.data
        except Exception as e:
            print(f"❌ Pending Feedback Fetch Failed: {e}")
            return []

    def admin_mark_feedback_sent(self, result_ids):
        """
        ADMIN: Marks a list of result IDs as feedback_sent=True
        """
        if not self.admin_supabase or not result_ids: return False
        try:
            self.admin_supabase.table('quiz_results').update({'feedback_sent': True}).in_('id', result_ids).execute()
            print(f"✅ Marked {len(result_ids)} results as feedback sent.")
            return True
        except Exception as e:
            print(f"❌ Feedback Mark Failed: {e}")
            return False


