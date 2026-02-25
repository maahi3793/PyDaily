import streamlit as st
import requests

def get_remote_ip():
    """
    Gets the client's PUBLIC IP address.
    
    Strategy:
    1. Primary: Use a free public IP API (works everywhere, returns the real public IP).
    2. Fallback: Try Streamlit's X-Forwarded-For header (works on Streamlit Cloud).
    
    The old method used _get_websocket_headers() which returned private IPs (192.x.x.x)
    on home WiFi, making geo-lookup impossible.
    """
    # 1. Primary: Public IP API (fast, reliable, returns just the IP string)
    try:
        resp = requests.get("https://api.ipify.org", timeout=2)
        if resp.status_code == 200:
            ip = resp.text.strip()
            if ip and not ip.startswith("192.") and not ip.startswith("10.") and not ip.startswith("172."):
                return ip
    except Exception:
        pass
    
    # 2. Fallback: Streamlit headers (works on Streamlit Cloud)
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        if headers:
            x_forwarded = headers.get("X-Forwarded-For")
            if x_forwarded:
                return x_forwarded.split(",")[0].strip()
            return headers.get("X-Real-Ip")
    except Exception:
        pass
    
    return None

def get_user_agent():
    """
    Extracts User-Agent string.
    """
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        if headers:
            return headers.get("User-Agent")
    except:
        pass
    return None

