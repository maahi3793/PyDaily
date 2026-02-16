import flet as ft
from html.parser import HTMLParser
import re

class HtmlToFlet(HTMLParser):
    def __init__(self, theme="dark"):
        super().__init__()
        self.theme = theme
        self.controls = []  # List of top-level controls
        
        # State
        self.current_spans = [] # For accumulating text spans inside a block (p, h1, etc.)
        self.current_block_type = None # 'p', 'h1', 'li', etc.
        self.style_stack = []   # Stack of style dicts {color, weight, etc.}
        self.link_url = None
        self.list_depth = 0
        self.in_pre = False
        
        # Theme colors
        self.text_color = ft.Colors.WHITE if theme == "dark" else ft.Colors.BLACK
        self.accent_color = ft.Colors.CYAN_400 if theme == "dark" else ft.Colors.CYAN_700
        
    def render(self, html_text):
        self.feed(html_text)
        self.flush_block() # Flush any remaining text
        return ft.Column(self.controls, spacing=2, scroll=None)

    def parse_style(self, style_str):
        """Parses inline style='key:value;...' into a dict"""
        style = {}
        if not style_str: return style
        for item in style_str.split(';'):
            if ':' in item:
                k, v = item.split(':', 1)
                k = k.strip().lower()
                v = v.strip()
                style[k] = v
        return style

    def flush_block(self):
        """Ends the current text block and creates a Flet Control"""
        if not self.current_spans:
            return

        # Determine Text Style based on current_block_type
        size = 16
        weight = ft.FontWeight.NORMAL
        color = self.text_color
        font_family = "Roboto"
        
        if self.current_block_type == 'h1':
            size = 32; weight = ft.FontWeight.BOLD; font_family = "Merriweather"
        elif self.current_block_type == 'h2':
            size = 26; weight = ft.FontWeight.BOLD; color = self.accent_color; font_family = "Merriweather"
        elif self.current_block_type == 'h3':
            size = 22; weight = ft.FontWeight.BOLD
        elif self.current_block_type == 'h4':
            size = 18; weight = ft.FontWeight.BOLD; color = ft.Colors.CYAN_100 # Brighter
        elif self.current_block_type == 'blockquote':
            color = ft.Colors.BLUE_100
            
        # Create Text Control
        # If it's a list item, prepend bullet
        prefix = ""
        if self.current_block_type == 'ul_li':
            prefix = "• "
        elif self.current_block_type == 'ol_li':
            prefix = "1. "

        if prefix:
             self.current_spans.insert(0, ft.TextSpan(prefix))

        # Specialized Containers
        if self.in_pre:
             full_text = "".join([s.text for s in self.current_spans])
             code_container = ft.Container(
                 content=ft.Text(full_text, font_family="Roboto Mono", color=ft.Colors.GREEN_300, size=14),
                 bgcolor="#1e293b" if self.theme == "dark" else "#f0f0f0",
                 padding=15,
                 border_radius=8,
                 border=ft.Border.all(1, "#334155")
             )
             self.controls.append(code_container)
        elif self.current_block_type == 'blockquote':
             # Callout Style
             self.controls.append(
                 ft.Container(
                     content=ft.Text(spans=self.current_spans, color=ft.Colors.WHITE, italic=True),
                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
                     padding=15,
                     border=ft.Border(left=ft.BorderSide(4, ft.Colors.BLUE_400)),
                     border_radius=4
                 )
             )
        else:
            # Filter empty text blocks to prevent huge gaps
            # check if spans actually have content
            has_content = any(s.text.strip() for s in self.current_spans)
            if not has_content and not prefix:
                self.current_spans = []
                self.current_block_type = None
                return

            # Force Header Colors in Dark Mode to ensure visibility
            if self.theme == 'dark':
                if self.current_block_type == 'h1': color = ft.Colors.WHITE
                elif self.current_block_type == 'h2': color = ft.Colors.CYAN_200
                elif self.current_block_type == 'h3': color = ft.Colors.AMBER_200

            txt = ft.Text(
                spans=self.current_spans,
                size=size,
                weight=weight,
                color=color,
                font_family=font_family,
                selectable=True
            )
            # Add some spacing for headers
            if self.current_block_type in ['h1', 'h2']:
                self.controls.append(ft.Container(content=txt, margin=ft.margin.only(top=15, bottom=5)))
            else:
                self.controls.append(txt)
            
        self.current_spans = []
        self.current_block_type = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        style = self.parse_style(attrs.get('style', ''))
        
        # Push standard styles
        current_style = {}
        # Only accept inline color if it's NOT a header (headers need theme consistency)
        # And if not in dark mode (where inline colors often fail)
        if 'color' in style: 
             if tag not in ['h1','h2','h3'] and self.theme != 'dark':
                current_style['color'] = style['color']
        
        self.current_spans = []
        self.current_block_type = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        style = self.parse_style(attrs.get('style', ''))
        
        # Push standard styles
        current_style = {}
        if 'color' in style: 
             if tag not in ['h1','h2','h3'] and self.theme != 'dark':
                current_style['color'] = style['color']
        
        if tag == 'blockquote':
            self.flush_block()
            self.current_block_type = 'blockquote' 
            # We don't need a strict boolean if we check block type, 
            # but let's be safe if p tags try to override it.
            # actually, current_block_type is overwritten by p in current logic.
            # So we DO need special handling.
            
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'li']:
             # These hard-break quotes usually.
             self.flush_block()
             self.current_block_type = tag
             if tag == 'li': self.current_block_type = 'ul_li'
             
        elif tag == 'p':
            if self.current_block_type == 'blockquote':
                # Nested p in blockquote -> just a newline
                if self.current_spans: self.current_spans.append(ft.TextSpan("\n\n"))
            else:
                self.flush_block()
                self.current_block_type = 'p'

        elif tag in ['ul', 'ol']:
            self.flush_block()
            self.list_depth += 1
            
        elif tag == 'pre':
            self.flush_block()
            self.in_pre = True
            
        elif tag == 'br':
            self.current_spans.append(ft.TextSpan("\n"))
            
        elif tag == 'img':
             # If inside blockquote, we might want to temporarily flush or just append?
             # For now, let's flush to be safe images are big.
             self.flush_block()
             src = attrs.get('src')
             alt = attrs.get('alt', 'Image')
             if "IMG_CH01_01" in alt or "IMG_CH01_01" in str(attrs):
                  src = "assets/print_flow.png"
             
             if src:
                 self.controls.append(ft.Image(src=src, fit="contain", border_radius=8, tooltip=alt))

        if tag in ['strong', 'b']: current_style['weight'] = ft.FontWeight.BOLD
        if tag in ['em', 'i']: current_style['italic'] = True
        if tag == 'a': 
            self.link_url = attrs.get('href')
            current_style['color'] = ft.Colors.BLUE_400
            current_style['decoration'] = ft.TextDecoration.UNDERLINE

        self.style_stack.append(current_style)

    def handle_endtag(self, tag):
        if tag == 'blockquote':
             self.flush_block()
        elif tag == 'p':
             if self.current_block_type == 'blockquote':
                 pass # Don't flush, just end of para line break (added at start of next p usually)
             else:
                 self.flush_block()
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'li']:
             self.flush_block()
        elif tag in ['ul', 'ol']:
             self.list_depth -= 1
        elif tag == 'pre':
             self.flush_block()
             self.in_pre = False
        
        if self.style_stack:
            self.style_stack.pop()
        
        if tag == 'a':
            self.link_url = None

    def handle_data(self, data):
        if not data: return
        
        # Resolve current styles
        t_style = ft.TextStyle()
        if self.style_stack:
             # Merge styles
             combined = {}
             for s in self.style_stack:
                 combined.update(s)
             
             if 'color' in combined: t_style.color = combined['color']
             if 'weight' in combined: t_style.weight = combined['weight']
             if 'italic' in combined: t_style.italic = True
             if 'decoration' in combined: t_style.decoration = combined['decoration']

        span = ft.TextSpan(
            text=data,
            style=t_style,
            url=self.link_url,
            on_enter=None # Hover cursor?
        )
        self.current_spans.append(span)

def render_html(html_content, theme="dark"):
    parser = HtmlToFlet(theme)
    return parser.render(html_content)
