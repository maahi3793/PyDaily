import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os
import pandas as pd

class SheetsManager:
    def __init__(self, key_file="service_account.json", sheet_name="PyDaily Database"):
        self.scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        
        self.key_file = key_file
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None

        if os.path.exists(self.key_file) or os.environ.get('GOOGLE_CREDENTIALS_JSON'):
            print(f"[INFO] Credentials found (File or Env). Connecting...")
            self.connect()
        else:
            print(f"[ERROR] Service Account File NOT Found at: {os.path.abspath(self.key_file)} AND no Env Var found.")
            logging.warning(f"SheetsManager: Credentials missing. Running in offline/json mode.")

    def connect(self):
        try:
            print("[INFO] Attempting to connect to Google Sheets API...")
            
            # Helper to parse Env Var if file missing
            import json
            
            if os.path.exists(self.key_file):
                print(f"[INFO] Using File: {self.key_file}")
                creds = ServiceAccountCredentials.from_json_keyfile_name(self.key_file, self.scope)
            elif os.environ.get('GOOGLE_CREDENTIALS_JSON'):
                print("[INFO] Using ENV VAR: GOOGLE_CREDENTIALS_JSON")
                key_dict = json.loads(os.environ.get('GOOGLE_CREDENTIALS_JSON'))
                creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, self.scope)
            else:
                 raise FileNotFoundError("No 'service_account.json' and no 'GOOGLE_CREDENTIALS_JSON' env var found.")

            self.client = gspread.authorize(creds)
            print("[INFO] Auth Successful. Opening Sheet...")
            
            # Open the sheet
            self.sheet = self.client.open(self.sheet_name).sheet1
            print(f"[INFO] Connected to Sheet: '{self.sheet_name}'")
            self.ensure_headers()
            logging.info("SheetsManager: Connected to Google Sheets!")
        except Exception as e:
            print(f"[ERROR] Connection Failed: {e}")
            logging.error(f"SheetsManager Connection Failed: {e}")

    def ensure_headers(self):
        try:
            # Check row 1
            headers = self.sheet.row_values(1)
            expected = ["name", "email", "day", "status"]
            
            # If empty or mistmatched, overwrite strict headers
            if not headers or headers != expected:
                print(f"[WARN] Headers mismatch. Found: {headers}. Enforcing standard headers...")
                # We won't clear, just update row 1 to be safe
                # Note: valid gspread call to update first row
                for i, col_name in enumerate(expected):
                    self.sheet.update_cell(1, i+1, col_name)
                print("[INFO] Headers fixed: name, email, day, status")
        except Exception as e:
            print(f"[ERROR] Could not verify headers: {e}")

    def get_all_contacts(self):
        if not self.sheet:
            print("[WARN] Sheet not connected, skipping fetch.")
            return []
        try:
            # Get all records as list of dicts
            return self.sheet.get_all_records()
        except Exception as e:
            print(f"[ERROR] Error fetching contacts: {e}")
            logging.error(f"Error fetching contacts from Sheet: {e}")
            return []

    def add_contact(self, name, email):
        if not self.sheet: 
            print("[WARN] Sheet not connected, cannot add contact.")
            return False
        try:
            # Check for duplicate
            contacts = self.get_all_contacts()
            for c in contacts:
                if c['email'] == email:
                    print(f"[WARN] Duplicate email found: {email}")
                    return False
            
            # Add Row: [name, email, day, status]
            print(f"[INFO] Appending row for {email}...")
            self.sheet.append_row([name, email, 1, "pending"])
            print("[INFO] Row added successfully.")
            return True
        except Exception as e:
            print(f"[ERROR] Error adding contact: {e}")
            logging.error(f"Error adding contact to Sheet: {e}")
            return False

    def update_status(self, email, day=None, status=None):
        if not self.sheet: return
        try:
            # Find row number
            cell = self.sheet.find(email)
            if not cell:
                return

            row = cell.row
            
            # Assuming columns: A=Name, B=Email, C=Day, D=Status
            # But get_all_records uses headers. 
            # Safest is to rely on fixed column indices if we control the sheet creation, 
            # or map headers. Let's assume standard Schema: Name, Email, Day, Status
            
            if day:
                self.sheet.update_cell(row, 3, day)
            if status:
                self.sheet.update_cell(row, 4, status)
                
        except Exception as e:
            logging.error(f"Error updating contact in Sheet: {e}")
            
    def delete_contact(self, email):
         if not self.sheet: return
         try:
            cell = self.sheet.find(email)
            if cell:
                self.sheet.delete_rows(cell.row)
         except Exception as e:
             logging.error(f"Error deleting contact: {e}")
