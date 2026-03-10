"""
Skill Tree Component
Modern, animated SVG visualization of the learning journey.
Uses a constellation/neural network aesthetic with glowing nodes.
"""
import streamlit as st
from backend import curriculum

def get_topic_nodes():
    """Returns topic nodes organized by phase for the skill tree."""
    return [
        # Phase 1: Foundations (Green)
        {"id": 1, "name": "Variables", "phase": 1, "color": "#10B981", "x": 100, "y": 80},
        {"id": 2, "name": "Data Types", "phase": 1, "color": "#10B981", "x": 200, "y": 60},
        {"id": 3, "name": "Operators", "phase": 1, "color": "#10B981", "x": 300, "y": 80},
        {"id": 4, "name": "Strings", "phase": 1, "color": "#10B981", "x": 180, "y": 140},
        {"id": 5, "name": "Lists", "phase": 1, "color": "#10B981", "x": 280, "y": 140},
        {"id": 6, "name": "Loops", "phase": 1, "color": "#10B981", "x": 230, "y": 200},
        
        # Phase 2: Core Skills (Blue)
        {"id": 7, "name": "Functions", "phase": 2, "color": "#3B82F6", "x": 400, "y": 100},
        {"id": 8, "name": "Modules", "phase": 2, "color": "#3B82F6", "x": 500, "y": 80},
        {"id": 9, "name": "File I/O", "phase": 2, "color": "#3B82F6", "x": 450, "y": 160},
        {"id": 10, "name": "Exceptions", "phase": 2, "color": "#3B82F6", "x": 550, "y": 140},
        
        # Phase 3: OOP (Purple)
        {"id": 11, "name": "Classes", "phase": 3, "color": "#8B5CF6", "x": 650, "y": 100},
        {"id": 12, "name": "Inheritance", "phase": 3, "color": "#8B5CF6", "x": 750, "y": 80},
        {"id": 13, "name": "Polymorphism", "phase": 3, "color": "#8B5CF6", "x": 700, "y": 160},
        
        # Phase 4: CS Fundamentals (Amber)
        {"id": 14, "name": "Big O", "phase": 4, "color": "#F59E0B", "x": 100, "y": 280},
        {"id": 15, "name": "Arrays", "phase": 4, "color": "#F59E0B", "x": 200, "y": 260},
        {"id": 16, "name": "Linked Lists", "phase": 4, "color": "#F59E0B", "x": 300, "y": 280},
        {"id": 17, "name": "Trees", "phase": 4, "color": "#F59E0B", "x": 250, "y": 340},
        {"id": 18, "name": "Graphs", "phase": 4, "color": "#F59E0B", "x": 150, "y": 340},
        
        # Phase 5: Pythonic (Pink)
        {"id": 19, "name": "Generators", "phase": 5, "color": "#EC4899", "x": 450, "y": 280},
        {"id": 20, "name": "Decorators", "phase": 5, "color": "#EC4899", "x": 550, "y": 260},
        {"id": 21, "name": "Context Mgr", "phase": 5, "color": "#EC4899", "x": 500, "y": 340},
        
        # Phase 6: Professional (Teal)
        {"id": 22, "name": "Async", "phase": 6, "color": "#14B8A6", "x": 700, "y": 280},
        {"id": 23, "name": "APIs", "phase": 6, "color": "#14B8A6", "x": 750, "y": 340},
        {"id": 24, "name": "Testing", "phase": 6, "color": "#14B8A6", "x": 650, "y": 340},
    ]


def get_connections():
    """Returns connections between nodes (edges in the graph)."""
    return [
        # Phase 1 flow
        (1, 2), (2, 3), (2, 4), (3, 5), (4, 6), (5, 6),
        # Phase 1 to 2
        (6, 7),
        # Phase 2 flow
        (7, 8), (7, 9), (8, 10), (9, 10),
        # Phase 2 to 3
        (10, 11),
        # Phase 3 flow
        (11, 12), (11, 13), (12, 13),
        # Phase 3 to 4 (jump down)
        (13, 14),
        # Phase 4 flow
        (14, 15), (15, 16), (15, 17), (14, 18), (17, 18), (16, 17),
        # Phase 4 to 5
        (17, 19),
        # Phase 5 flow
        (19, 20), (19, 21), (20, 21),
        # Phase 5 to 6
        (21, 22),
        # Phase 6 flow
        (22, 23), (22, 24), (23, 24),
    ]


def render_skill_tree(current_day: int):
    """
    Renders an interactive SVG skill tree with glowing nodes.
    Nodes are lit up based on progress.
    """
    nodes = get_topic_nodes()
    connections = get_connections()
    
    # Determine which phases are unlocked
    phase_info, _ = curriculum.get_phase_info(current_day)
    
    # Generate SVG
    svg_width = 850
    svg_height = 400
    
    # Build connection lines
    lines_svg = ""
    for (from_id, to_id) in connections:
        from_node = next((n for n in nodes if n['id'] == from_id), None)
        to_node = next((n for n in nodes if n['id'] == to_id), None)
        if from_node and to_node:
            # Determine if connection is unlocked
            is_unlocked = from_node['phase'] <= phase_info and to_node['phase'] <= phase_info
            stroke_color = from_node['color'] if is_unlocked else "#334155"
            opacity = "0.8" if is_unlocked else "0.2"
            lines_svg += f'''
            <line x1="{from_node['x']}" y1="{from_node['y']}" 
                  x2="{to_node['x']}" y2="{to_node['y']}" 
                  stroke="{stroke_color}" stroke-width="2" opacity="{opacity}"/>
            '''
    
    # Build nodes
    nodes_svg = ""
    for node in nodes:
        is_unlocked = node['phase'] <= phase_info
        fill_color = node['color'] if is_unlocked else "#1e293b"
        stroke_color = node['color'] if is_unlocked else "#334155"
        text_color = "#f8fafc" if is_unlocked else "#64748b"
        glow_class = "glow" if is_unlocked else ""
        
        nodes_svg += f'''
        <g class="node {glow_class}">
            <circle cx="{node['x']}" cy="{node['y']}" r="25" 
                    fill="{fill_color}" stroke="{stroke_color}" stroke-width="3"/>
            <text x="{node['x']}" y="{node['y'] + 45}" 
                  fill="{text_color}" text-anchor="middle" font-size="11" font-weight="500">
                {node['name']}
            </text>
        </g>
        '''
    
    # Complete SVG with animations
    svg = f'''
    <style>
        .skill-tree-container {{
            background: radial-gradient(ellipse at center, #1e293b 0%, #0f172a 100%);
            border-radius: 16px;
            padding: 20px;
            overflow-x: auto;
        }}
        .glow circle {{
            filter: drop-shadow(0 0 8px currentColor);
            animation: pulse 3s ease-in-out infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ filter: drop-shadow(0 0 5px currentColor); }}
            50% {{ filter: drop-shadow(0 0 15px currentColor); }}
        }}
        .node {{
            transition: transform 0.3s ease;
        }}
        .node:hover {{
            transform: scale(1.1);
        }}
    </style>
    <div class="skill-tree-container">
        <svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
            <!-- Connection Lines -->
            {lines_svg}
            <!-- Nodes -->
            {nodes_svg}
            
            <!-- Legend -->
            <g transform="translate(20, 380)">
                <text fill="#64748b" font-size="10">
                    🟢 Unlocked  |  ⚫ Locked  |  Current Phase: {phase_info}
                </text>
            </g>
        </svg>
    </div>
    '''
    
    st.markdown("### 🌌 Your Skill Constellation")
    st.caption("Watch your knowledge nodes light up as you progress!")
    
    import streamlit.components.v1 as components
    components.html(svg, height=450, scrolling=False)
