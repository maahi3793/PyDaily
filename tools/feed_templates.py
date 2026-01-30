def get_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .feed-card {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 2rem;
        border-radius: 24px;
        position: relative;
        overflow: hidden;
        font-family: 'Outfit', sans-serif;
    }
    
    /* 1. GRADIENT CARD (Tips/Facts) */
    .style-gradient {
        background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
        color: white;
    }
    .style-gradient h2 {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 1rem;
        background: rgba(0,0,0,0.2);
        padding: 10px 20px;
        border-radius: 12px;
        display: inline-block;
        backdrop-filter: blur(5px);
    }
    .style-gradient p {
        font-size: 1.4rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* 2. NEON CODE (Snippets) */
    .style-code {
        background: #0f172a;
        border: 1px solid #334155;
    }
    .terminal-window {
        background: #1e293b;
        border-radius: 12px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        overflow: hidden;
        margin-top: 1rem;
        border: 1px solid #475569;
    }
    .terminal-header {
        background: #334155;
        padding: 10px 15px;
        display: flex;
        gap: 8px;
    }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-r { background: #ef4444; }
    .dot-y { background: #eab308; }
    .dot-g { background: #22c55e; }
    
    .style-code pre {
        margin: 0;
        padding: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        color: #e2e8f0;
        overflow-x: auto;
    }
    
    /* 3. IMAGE CARD */
    .style-image {
        background: black;
        padding: 0;
    }
    .img-container {
        width: 100%;
        height: 100%;
        background-position: center;
        background-size: cover;
        position: relative;
    }
    .img-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
        padding: 40px 20px 20px 20px;
        color: white;
    }
    </style>
    """

def render_gradient_card(topic, title, content):
    css = get_css()
    return f"""
    {css}
    <div class="feed-card style-gradient">
        <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.9; margin-bottom: 20px;">
            {topic}
        </div>
        <h2>{title}</h2>
        <p>{content}</p>
        <div style="font-size: 5rem; position: absolute; top: -20px; right: -20px; opacity: 0.2;">
            🧠
        </div>
    </div>
    """

def render_code_card(topic, title, code, explanation):
    css = get_css()
    # simplistic html usage for code to avoid messing up f-strings
    return f"""
    {css}
    <div class="feed-card style-code">
        <h3 style="color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">{topic}</h3>
        <h1 style="color: #60a5fa; margin: 0 0 1rem 0;">{title}</h1>
        <p style="font-size: 1.1rem; color: #cbd5e1;">{explanation}</p>
        
        <div class="terminal-window">
            <div class="terminal-header">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>
            <pre><code>{code}</code></pre>
        </div>
    </div>
    """

def render_image_card(topic, title, image_url, caption):
    css = get_css()
    return f"""
    {css}
    <div class="feed-card style-image">
        <div class="img-container" style="background-image: url('{image_url}');">
            <div class="img-overlay">
                <span style="background: #ef4444; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; text-transform: uppercase;">
                    {topic}
                </span>
                <h1 style="margin: 10px 0 5px 0; font-size: 2rem;">{title}</h1>
                <p style="font-size: 1.1rem; color: #e2e8f0;">{caption}</p>
            </div>
        </div>
    </div>
    """
