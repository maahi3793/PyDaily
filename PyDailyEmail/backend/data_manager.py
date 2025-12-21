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

# --- Contacts ---
def get_contacts():
    return load_json(CONTACTS_FILE, [])

def add_contact(name, email):
    contacts = get_contacts()
    # Check duplicate
    for c in contacts:
        if c['email'] == email:
            return False
    contacts.append({"name": name, "email": email})
    save_json(CONTACTS_FILE, contacts)
    return True

def delete_contact(email):
    contacts = get_contacts()
    new_contacts = [c for c in contacts if c['email'] != email]
    save_json(CONTACTS_FILE, new_contacts)

# --- Config ---
def get_config():
    return load_json(CONFIG_FILE, {"gemini_key": "", "email_address": "", "email_password": ""})

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
