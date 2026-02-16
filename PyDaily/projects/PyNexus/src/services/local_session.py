import json
import os
from pathlib import Path

class LocalSession:
    """
    Robust local session storage for Desktop App.
    Stores auth token and preferences in a hidden JSON file in the user's home directory.
    This bypasses Flet's client_storage which can be unreliable in debug/script modes.
    """
    def __init__(self):
        self.app_dir = Path.home() / ".pynexus_data"
        self.session_file = self.app_dir / "session.json"
        
        # Ensure dir exists
        try:
            self.app_dir.mkdir(exist_ok=True)
        except Exception as e:
            print(f"Warning: Failed to create session dir: {e}")

    def save(self, key, value):
        data = self.load_all()
        data[key] = value
        self._write(data)

    def get(self, key):
        data = self.load_all()
        return data.get(key)
    
    def remove(self, key):
        data = self.load_all()
        if key in data:
            del data[key]
            self._write(data)
            
    def clear(self):
        self._write({})

    def load_all(self):
        if not self.session_file.exists():
            return {}
        try:
            with open(self.session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading session: {e}")
            return {}

    def _write(self, data):
        try:
            with open(self.session_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error writing session: {e}")
