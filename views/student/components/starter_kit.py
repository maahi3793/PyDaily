"""
Day 0 Starter Kit Component
Provides a downloadable HTML starter guide for new students.
"""
import streamlit as st
import base64

def get_starter_kit_html():
    """Returns HTML content for the Python Starter Kit."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐍 PyDaily Starter Kit</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
            line-height: 1.6;
            padding: 40px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { 
            font-size: 2.5rem; 
            margin-bottom: 10px; 
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        h2 { 
            font-size: 1.5rem; 
            color: #3b82f6; 
            margin: 30px 0 15px; 
            border-bottom: 2px solid #334155;
            padding-bottom: 10px;
        }
        h3 { color: #94a3b8; margin: 20px 0 10px; }
        p, li { color: #cbd5e1; }
        .card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
        }
        code {
            background: #0f172a;
            color: #f59e0b;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
        }
        pre {
            background: #0f172a;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
        }
        pre code { padding: 0; background: none; }
        .badge {
            display: inline-block;
            background: #3b82f6;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-right: 8px;
        }
        ul { padding-left: 20px; }
        li { margin: 8px 0; }
        .shortcut { 
            display: grid; 
            grid-template-columns: 1fr 2fr; 
            gap: 10px;
            margin: 10px 0;
        }
        .shortcut kbd {
            background: #334155;
            padding: 5px 10px;
            border-radius: 4px;
            font-family: monospace;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #334155;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 PyDaily Starter Kit</h1>
        <p>Welcome to your Python journey! This guide will help you set up your environment.</p>
        
        <h2>📥 Step 1: Install Python</h2>
        <div class="card">
            <h3>Windows</h3>
            <ol>
                <li>Go to <a href="https://www.python.org/downloads/" style="color:#3b82f6;">python.org/downloads</a></li>
                <li>Download Python 3.11+ (latest stable)</li>
                <li>Run installer → <strong>Check "Add Python to PATH"</strong></li>
                <li>Click "Install Now"</li>
            </ol>
            
            <h3>macOS</h3>
            <pre><code>brew install python3</code></pre>
            
            <h3>Linux</h3>
            <pre><code>sudo apt update && sudo apt install python3 python3-pip</code></pre>
        </div>
        
        <h2>✅ Step 2: Verify Installation</h2>
        <div class="card">
            <p>Open Terminal/Command Prompt and run:</p>
            <pre><code>python --version</code></pre>
            <p>You should see: <code>Python 3.11.x</code> (or higher)</p>
        </div>
        
        <h2>💻 Step 3: Choose Your Editor</h2>
        <div class="card">
            <p><span class="badge">Recommended</span> <strong>VS Code</strong></p>
            <ol>
                <li>Download from <a href="https://code.visualstudio.com/" style="color:#3b82f6;">code.visualstudio.com</a></li>
                <li>Install the <strong>Python Extension</strong> by Microsoft</li>
            </ol>
            
            <h3>Alternatives</h3>
            <ul>
                <li><strong>PyCharm Community</strong> - Full IDE (heavier)</li>
                <li><strong>Thonny</strong> - Beginner-friendly (lighter)</li>
                <li><strong>Replit.com</strong> - Browser-based (no install)</li>
            </ul>
        </div>
        
        <h2>🚀 Step 4: Hello World!</h2>
        <div class="card">
            <p>Create a file called <code>hello.py</code> and add:</p>
            <pre><code>print("Hello, PyDaily! 🐍")</code></pre>
            <p>Run it in terminal:</p>
            <pre><code>python hello.py</code></pre>
        </div>
        
        <h2>⌨️ Essential Keyboard Shortcuts (VS Code)</h2>
        <div class="card">
            <div class="shortcut"><kbd>Ctrl + S</kbd> <span>Save file</span></div>
            <div class="shortcut"><kbd>Ctrl + `</kbd> <span>Open terminal</span></div>
            <div class="shortcut"><kbd>F5</kbd> <span>Run Python file</span></div>
            <div class="shortcut"><kbd>Ctrl + /</kbd> <span>Comment/Uncomment</span></div>
            <div class="shortcut"><kbd>Ctrl + D</kbd> <span>Select next occurrence</span></div>
            <div class="shortcut"><kbd>Ctrl + Shift + K</kbd> <span>Delete line</span></div>
            <div class="shortcut"><kbd>Alt + ↑/↓</kbd> <span>Move line up/down</span></div>
        </div>
        
        <h2>📚 Quick Reference</h2>
        <div class="card">
            <h3>Basic Syntax</h3>
            <pre><code># Variables
name = "PyDaily"
age = 1

# Print
print(f"Hello, {name}!")

# Conditionals
if age >= 1:
    print("You're ready!")

# Loops
for i in range(5):
    print(i)</code></pre>
        </div>
        
        <h2>🎯 Your First Week Goals</h2>
        <div class="card">
            <ul>
                <li>✅ Install Python & VS Code</li>
                <li>✅ Run your first "Hello World"</li>
                <li>📖 Complete Day 1-3 lessons</li>
                <li>🧠 Take your first quiz on Day 3</li>
                <li>💬 Bookmark any confusing topics</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Made with ❤️ by PyDaily | Your journey starts now!</p>
            <p>Dashboard: <a href="https://pydaily.streamlit.app" style="color:#3b82f6;">pydaily.streamlit.app</a></p>
        </div>
    </div>
</body>
</html>
"""


def render_starter_kit_download():
    """Renders a download button for the starter kit."""
    
    st.markdown("""
    <style>
    .kit-card {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    .kit-icon { font-size: 3rem; margin-bottom: 15px; }
    .kit-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; }
    .kit-desc { opacity: 0.9; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="kit-card">
        <div class="kit-icon">🎁</div>
        <div class="kit-title">Day 0 Starter Kit</div>
        <div class="kit-desc">Get your Python environment ready before Day 1!</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate downloadable HTML
    html_content = get_starter_kit_html()
    b64 = base64.b64encode(html_content.encode()).decode()
    
    # Center the download button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Starter Kit",
            data=html_content,
            file_name="PyDaily_Starter_Kit.html",
            mime="text/html",
            use_container_width=True
        )
    
    st.caption("📖 Open the downloaded file in your browser to view the guide!")
