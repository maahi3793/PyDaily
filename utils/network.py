import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers

def get_remote_ip():
    """
    Attempts to get the client's IP address from Streamlit headers.
    Works on Streamlit Cloud via 'X-Forwarded-For'.
    """
    try:
        headers = _get_websocket_headers()
        if headers:
            # X-Forwarded-For: client, proxy1, proxy2
            x_forwarded = headers.get("X-Forwarded-For")
            if x_forwarded:
                return x_forwarded.split(",")[0].strip()
            
            # Fallback for some proxies
            return headers.get("X-Real-Ip")
            
    except Exception as e:
        return None
    return None
