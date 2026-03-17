import os
import sys
import webview

def get_base_path():
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    base_path = get_base_path()
    entry_point = os.path.join(base_path, 'index.html')
    
    # Create the window
    window = webview.create_window('PyMandir \u2014 Temple of Knowledge', entry_point, width=1536, height=864, min_size=(1024, 600))
    
    # Start app. http_server=True creates a local server on a random port 
    # to serve local assets properly (fixes CORS/IFrame API issues)
    webview.start(http_server=True)
