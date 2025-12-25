import json
import os

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTACTS_FILE = os.path.join(DATA_DIR, 'contacts.json')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')
STATE_FILE = os.path.join(DATA_DIR, 'state.json')

def load_json(filepath, default=None):
    if default is None: default = {}
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return default

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)



# --- Contacts (Supabase Backend) ---
from backend.db_supabase import SupabaseManager

# Global DB Instance (for direct access)
db = SupabaseManager()

def get_contacts():
    # 🚀 Now fetching from Supabase directly
    db = SupabaseManager()
    return db.admin_get_all_students()

def add_contact(name, email, password="ChangeMe123!"):
    db = SupabaseManager()
    success, msg = db.admin_create_student(email, name, password)
    return success

def delete_contact(email):
    db = SupabaseManager()
    db.admin_delete_student(email)

def update_contact_status(email, day=None, status=None):
    db = SupabaseManager()
    return db.admin_update_student_progress(email, day, status)

# --- Config ---
def get_config():
    config = load_json(CONFIG_FILE, {"gemini_key": "", "email_address": "", "email_password": "", "test_mode": False, "admin_email": ""})
    
    # Priority: Env Vars > Config File (Safety for Cloud)
    if not config.get('gemini_key'):
        config['gemini_key'] = os.environ.get('GEMINI_API_KEY', '')
    if not config.get('email_address'):
        config['email_address'] = os.environ.get('EMAIL_ADDRESS', '')
    if not config.get('email_password'):
        config['email_password'] = os.environ.get('EMAIL_PASSWORD', '')
    if not config.get('admin_email'):
        config['admin_email'] = os.environ.get('ADMIN_EMAIL', '') # Optional Env Var
        
    return config

def save_config(gemini_key, email_address, email_password, test_mode=False, admin_email=""):
    save_json(CONFIG_FILE, {
        "gemini_key": gemini_key, 
        "email_address": email_address, 
        "email_password": email_password,
        "test_mode": test_mode,
        "admin_email": admin_email
    })

# --- State ---
def get_state():
    return load_json(STATE_FILE, {"current_day": 1, "last_run": None})

def update_state(day=None, last_run=None):
    state = get_state()
    if day: state['current_day'] = day
    if last_run: state['last_run'] = last_run
    save_json(STATE_FILE, state)

# --- Admin Auth Ops ---
def admin_force_password_reset(email, new_password):
    from backend.db_supabase import SupabaseManager
    db = SupabaseManager()
    return db.admin_update_password(email, new_password)
