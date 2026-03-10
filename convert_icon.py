from PIL import Image
import os

# Define paths
icon_path = r"C:\Users\reach\.gemini\antigravity\brain\7e9d030a-5b84-4a4b-b027-9b416c05588e\pynexus_icon_1771353078772.png"
output_path = r"c:\Users\reach\.gemini\antigravity\scratch\relaunchpython\PyDaily\projects\PyNexus\assets\icon.ico"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

try:
    img = Image.open(icon_path)
    # Resize and save as ICO with multiple sizes for best scaling checking
    img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Successfully converted {icon_path} to {output_path}")
except Exception as e:
    print(f"Error converting icon: {e}")
