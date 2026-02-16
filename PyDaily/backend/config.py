import os
import json
from dotenv import load_dotenv

# Load local .env (if present)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, '.env')
load_dotenv(ENV_PATH)

CONFIG_FILE = os.path.join(ROOT_DIR, 'backend', 'config.json')

def load_json(filepath, default=None):
    if default is None: default = {}
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return default

def get_config():
    """
    Loads configuration from JSON file, Environment Variables, or Streamlit Secrets.
    Priority: Streamlit Secrets > Env Vars > Config File
    """
    # Default Config Structure
    config = load_json(CONFIG_FILE, {
        "gemini_key": "", 
        "email_address": "", 
        "email_password": "", 
        "test_mode": False, 
        "admin_email": ""
    })
    
    # 1. Environment Variables (Override File) - Standard for Cloud/GitHub Actions
    if 'SUPABASE_URL' in os.environ:
        config['supabase_url'] = os.environ['SUPABASE_URL']
    if 'SUPABASE_SERVICE_KEY' in os.environ:
        config['supabase_service_key'] = os.environ['SUPABASE_SERVICE_KEY']
    if 'GEMINI_API_KEY' in os.environ:
        config['gemini_key'] = os.environ['GEMINI_API_KEY']
    if 'EMAIL_ADDRESS' in os.environ:
        config['email_address'] = os.environ['EMAIL_ADDRESS']
    if 'EMAIL_PASSWORD' in os.environ:
        config['email_password'] = os.environ['EMAIL_PASSWORD']
    if 'ADMIN_EMAIL' in os.environ:
        config['admin_email'] = os.environ['ADMIN_EMAIL']

    # 2. Streamlit Secrets (Override Env/File) - Specific for Streamlit Cloud
    try:
        import streamlit as st
        if 'GEMINI_API_KEY' in st.secrets:
            config['gemini_key'] = st.secrets['GEMINI_API_KEY']
        if 'EMAIL_ADDRESS' in st.secrets:
            config['email_address'] = st.secrets['EMAIL_ADDRESS']
        if 'EMAIL_PASSWORD' in st.secrets:
            config['email_password'] = st.secrets['EMAIL_PASSWORD']
        if 'ADMIN_EMAIL' in st.secrets:
            config['admin_email'] = st.secrets['ADMIN_EMAIL']
        if 'SUPABASE_URL' in st.secrets:
            config['supabase_url'] = st.secrets['SUPABASE_URL']
        if 'SUPABASE_SERVICE_KEY' in st.secrets:
            config['supabase_service_key'] = st.secrets['SUPABASE_SERVICE_KEY']
    except:
        pass # Not running in Streamlit
    
    return config

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def save_config(gemini_key, email_address, email_password, test_mode=False, admin_email=""):
    save_json(CONFIG_FILE, {
        "gemini_key": gemini_key, 
        "email_address": email_address, 
        "email_password": email_password,
        "test_mode": test_mode,
        "admin_email": admin_email
    })
