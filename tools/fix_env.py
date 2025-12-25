
import os

def fix_env():
    env_path = '.env'
    if not os.path.exists(env_path):
        print(".env not found")
        return

    print(f"Reading {env_path}...")
    with open(env_path, 'rb') as f:
        raw = f.read()

    print(f"Original Byte Length: {len(raw)}")
    
    # PowerShell often adds BOM \xff\xfe or just null bytes for UTF-16
    # Simple fix for ASCII-compatible content: Remove null bytes
    # This turns "A\x00B\x00" (UTF-16) into "AB" (ASCII/UTF-8)
    clean = raw.replace(b'\x00', b'')
    
    # Also remove BOM if present at start (UTF-16 LE BOM is \xff\xfe)
    # But usually replacing \x00 handles the bulk. 
    # Let's decode to check validity
    try:
        text = clean.decode('utf-8')
        # Remove any lingering BOM characters from UTF-8 decode
        text = text.replace('\ufeff', '') 
        print("Decoded Successfully.")
        print("--- Content ---")
        print(text)
        print("---------------")
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("✅ Saved clean .env as UTF-8")
        
    except Exception as e:
        print(f"❌ Failed to decode: {e}")

if __name__ == "__main__":
    fix_env()
