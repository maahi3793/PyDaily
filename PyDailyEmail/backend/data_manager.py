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

from backend import sheets_manager

# Initialize Sheets Manager (Global)
sheets = sheets_manager.SheetsManager()

# --- Contacts ---
def get_contacts():
    # Priority: Google Sheets > JSON
    if sheets.sheet:
        return sheets.get_all_contacts()
    
    # Fallback to Local JSON
    return load_json(CONTACTS_FILE, [])

def add_contact(name, email):
    if sheets.sheet:
        return sheets.add_contact(name, email)
    
    # Fallback
    contacts = load_json(CONTACTS_FILE, [])
    for c in contacts:
        if c['email'] == email:
            return False
    contacts.append({"name": name, "email": email, "day": 1, "status": "pending"})
    save_json(CONTACTS_FILE, contacts)
    return True

def delete_contact(email):
    if sheets.sheet:
        sheets.delete_contact(email)
        return

    # Fallback
    contacts = load_json(CONTACTS_FILE, [])
    new_contacts = [c for c in contacts if c['email'] != email]
    save_json(CONTACTS_FILE, new_contacts)

def update_contact_status(email, day=None, status=None):
    if sheets.sheet:
        sheets.update_status(email, day, status)
        return

    # Fallback
    contacts = load_json(CONTACTS_FILE, [])
    for c in contacts:
        if c['email'] == email:
            if day: c['day'] = day
            if status: c['status'] = status
            break
    save_json(CONTACTS_FILE, contacts)

# --- Config ---
def get_config():
    config = load_json(CONFIG_FILE, {"gemini_key": "", "email_address": "", "email_password": ""})
    
    # Priority: Env Vars > Config File (Safety for Cloud)
    if not config.get('gemini_key'):
        config['gemini_key'] = os.environ.get('GEMINI_API_KEY', '')
    if not config.get('email_address'):
        config['email_address'] = os.environ.get('EMAIL_ADDRESS', '')
    if not config.get('email_password'):
        config['email_password'] = os.environ.get('EMAIL_PASSWORD', '')
        
    return config

def save_config(gemini_key, email_address, email_password):
    save_json(CONFIG_FILE, {"gemini_key": gemini_key, "email_address": email_address, "email_password": email_password})

# --- State ---
def get_state():
    return load_json(STATE_FILE, {"current_day": 1, "last_run": None})

def update_state(day=None, last_run=None):
    state = get_state()
    if day: state['current_day'] = day
    if last_run: state['last_run'] = last_run
    save_json(STATE_FILE, state)
