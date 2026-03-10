"""
Expert Skills Kit Component
Provides a downloadable roadmap of professional developer skills beyond Python.
Includes: Linux, Git, Docker, Cloud, Databases, APIs, Testing, etc.
"""
import streamlit as st
import base64

def get_expert_kit_html():
    """Returns HTML content for the Expert Skills Roadmap."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Python Developer Roadmap - Beyond the Basics</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
            line-height: 1.6;
            padding: 40px;
        }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { 
            font-size: 2.5rem; 
            margin-bottom: 10px; 
            background: linear-gradient(90deg, #f59e0b, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        h2 { 
            font-size: 1.5rem; 
            color: #f59e0b; 
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
        .skill-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        @media (max-width: 600px) {
            .skill-section { grid-template-columns: 1fr; }
        }
        .skill-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.3s, border-color 0.3s;
        }
        .skill-card:hover {
            transform: translateY(-5px);
            border-color: #f59e0b;
        }
        .skill-icon { font-size: 2rem; margin-bottom: 10px; }
        .skill-name { font-size: 1.2rem; font-weight: 700; color: #f8fafc; }
        .skill-desc { font-size: 0.9rem; color: #94a3b8; margin: 10px 0; }
        .skill-topics { font-size: 0.8rem; color: #64748b; }
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
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            margin-right: 5px;
        }
        .badge-essential { background: #10B981; color: white; }
        .badge-recommended { background: #3B82F6; color: white; }
        .badge-advanced { background: #8B5CF6; color: white; }
        .roadmap { 
            position: relative; 
            padding-left: 30px; 
        }
        .roadmap::before {
            content: '';
            position: absolute;
            left: 10px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(to bottom, #10B981, #3B82F6, #8B5CF6, #f59e0b);
        }
        .roadmap-item {
            position: relative;
            margin: 20px 0;
            padding-left: 20px;
        }
        .roadmap-item::before {
            content: '';
            position: absolute;
            left: -24px;
            top: 5px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #f59e0b;
            border: 3px solid #0f172a;
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
        <h1>🚀 Expert Python Developer Roadmap</h1>
        <p>Master these skills to become a professional Python developer.</p>
        
        <h2>🎯 Skill Categories</h2>
        <p>
            <span class="badge badge-essential">Essential</span> Must-know for any job
            <span class="badge badge-recommended">Recommended</span> Highly valuable
            <span class="badge badge-advanced">Advanced</span> Specialized skills
        </p>
        
        <div class="skill-section">
            <div class="skill-card">
                <div class="skill-icon">🐧</div>
                <div class="skill-name">Linux / Command Line</div>
                <div class="skill-desc">Navigate servers, automate tasks, deploy apps.</div>
                <div class="skill-topics"><span class="badge badge-essential">Essential</span> bash, ssh, grep, awk, cron, permissions</div>
            </div>
            
            <div class="skill-card">
                <div class="skill-icon">🌿</div>
                <div class="skill-name">Git & GitHub</div>
                <div class="skill-desc">Version control for collaborative development.</div>
                <div class="skill-topics"><span class="badge badge-essential">Essential</span> branches, merge, rebase, PRs, CI/CD</div>
            </div>
            
            <div class="skill-card">
                <div class="skill-icon">🐳</div>
                <div class="skill-name">Docker & Containers</div>
                <div class="skill-desc">Package and deploy apps consistently.</div>
                <div class="skill-topics"><span class="badge badge-recommended">Recommended</span> Dockerfile, compose, images, volumes</div>
            </div>
            
            <div class="skill-card">
                <div class="skill-icon">☁️</div>
                <div class="skill-name">Cloud Platforms</div>
                <div class="skill-desc">AWS, GCP, or Azure for production apps.</div>
                <div class="skill-topics"><span class="badge badge-recommended">Recommended</span> EC2, S3, Lambda, Cloud Functions</div>
            </div>
            
            <div class="skill-card">
                <div class="skill-icon">🗄️</div>
                <div class="skill-name">Databases</div>
                <div class="skill-desc">Store and query data efficiently.</div>
                <div class="skill-topics"><span class="badge badge-essential">Essential</span> PostgreSQL, SQLite, Redis, ORMs</div>
            </div>
            
            <div class="skill-card">
                <div class="skill-icon">🔌</div>
                <div class="skill-name">APIs & Web</div>
                <div class="skill-desc">Build and consume REST/GraphQL APIs.</div>
                <div class="skill-topics"><span class="badge badge-essential">Essential</span> Flask, FastAPI, requests, JSON</div>
            </div>
            
            <div class="skill-card">
                <div class="skill-icon">🧪</div>
                <div class="skill-name">Testing</div>
                <div class="skill-desc">Write reliable, maintainable code.</div>
                <div class="skill-topics"><span class="badge badge-essential">Essential</span> pytest, unittest, mocking, TDD</div>
            </div>
            
            <div class="skill-card">
                <div class="skill-icon">📊</div>
                <div class="skill-name">Data & Analytics</div>
                <div class="skill-desc">Process and visualize data.</div>
                <div class="skill-topics"><span class="badge badge-recommended">Recommended</span> pandas, numpy, matplotlib, SQL</div>
            </div>
        </div>
        
        <h2>📈 Recommended Learning Path</h2>
        <div class="card">
            <div class="roadmap">
                <div class="roadmap-item">
                    <strong>Month 1-2:</strong> Linux CLI + Git basics
                </div>
                <div class="roadmap-item">
                    <strong>Month 3-4:</strong> Databases (SQL) + APIs
                </div>
                <div class="roadmap-item">
                    <strong>Month 5-6:</strong> Testing + Docker
                </div>
                <div class="roadmap-item">
                    <strong>Month 7-8:</strong> Cloud deployment (pick one)
                </div>
                <div class="roadmap-item">
                    <strong>Month 9+:</strong> Specialize: Data Science, DevOps, or Backend
                </div>
            </div>
        </div>
        
        <h2>🔧 Essential Commands Cheatsheet</h2>
        <div class="card">
            <h3>Git</h3>
            <pre><code>git clone URL         # Clone repo
git checkout -b name  # Create branch
git add . && git commit -m "msg"
git push origin branch
git pull --rebase</code></pre>
            
            <h3>Linux</h3>
            <pre><code>ls -la               # List files
cd /path/to/dir      # Change directory
cat file.txt         # View file
grep "pattern" file  # Search in file
chmod +x script.sh   # Make executable
ssh user@server      # Connect to server</code></pre>
            
            <h3>Docker</h3>
            <pre><code>docker build -t name .        # Build image
docker run -p 8000:8000 name  # Run container
docker ps                      # List containers
docker-compose up -d           # Start services</code></pre>
        </div>
        
        <h2>📚 Learning Resources</h2>
        <div class="card">
            <ul>
                <li><strong>Linux:</strong> <a href="https://linuxjourney.com" style="color:#3b82f6;">linuxjourney.com</a></li>
                <li><strong>Git:</strong> <a href="https://learngitbranching.js.org" style="color:#3b82f6;">learngitbranching.js.org</a></li>
                <li><strong>Docker:</strong> <a href="https://docker-curriculum.com" style="color:#3b82f6;">docker-curriculum.com</a></li>
                <li><strong>AWS:</strong> <a href="https://aws.amazon.com/training/digital/" style="color:#3b82f6;">AWS Skill Builder (Free)</a></li>
                <li><strong>SQL:</strong> <a href="https://sqlbolt.com" style="color:#3b82f6;">sqlbolt.com</a></li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Made with ❤️ by PyDaily | Level up your skills!</p>
        </div>
    </div>
</body>
</html>
"""


def render_expert_kit_download():
    """Renders the Expert Skills Kit download card."""
    
    st.markdown("""
    <style>
    .expert-kit-card {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    .expert-kit-icon { font-size: 3rem; margin-bottom: 15px; }
    .expert-kit-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; }
    .expert-kit-desc { opacity: 0.9; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="expert-kit-card">
        <div class="expert-kit-icon">🚀</div>
        <div class="expert-kit-title">Expert Skills Roadmap</div>
        <div class="expert-kit-desc">Linux, Git, Docker, Cloud & more!</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate downloadable HTML
    html_content = get_expert_kit_html()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Roadmap",
            data=html_content,
            file_name="PyDaily_Expert_Skills_Roadmap.html",
            mime="text/html",
            use_container_width=True
        )
    
    st.caption("🔥 Skills every Python pro needs beyond just coding!")
