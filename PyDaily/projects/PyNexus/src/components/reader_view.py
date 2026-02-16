import flet as ft

class ReaderView(ft.Container):
    def __init__(self, content_text, title="User", theme="light", image_map=None):
        super().__init__()
        self.content_text = content_text
        self.title_text = title
        self.theme = theme
        self.image_map = image_map or {}

        # Styles based on theme
        bg_color = ft.Colors.WHITE
        text_color = ft.Colors.BLACK
        
        if self.theme == "dark":
            bg_color = "#1e1e1e"
            text_color = "#b3ffffff" # White-70
        elif self.theme == "sepia":
            bg_color = "#f4ecd8"
            text_color = "#5b4636"

        # Initialize Column with Title and Divider
        content_column = ft.Column(
            [
                ft.Text(self.title_text, size=24, weight="bold", color=text_color, font_family="Merriweather"),
                ft.Container(height=1, bgcolor=ft.Colors.with_opacity(0.1, text_color), margin=ft.margin.only(bottom=20)),
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )
        
        # Check if content is HTML (if not, assume Markdown)
        is_html = self.content_text.strip().startswith("<")

        # Resolve Image Placeholders
        if self.image_map:
            for pid, url in self.image_map.items():
                placeholder = f"<!-- IMAGE_PLACEHOLDER: {pid} -->"
                if placeholder in self.content_text:
                    replacement = f'<img src="{url}" alt="{pid}" style="max-width:100%; border-radius:8px;">'
                    self.content_text = self.content_text.replace(placeholder, replacement)
        
        # Fallback for manual assets
        if "IMG_CH01_01" in self.content_text and "IMG_CH01_01" not in self.image_map:
            self.content_text = self.content_text.replace(
                "<!-- IMAGE_PLACEHOLDER: IMG_CH01_01 -->", 
                '<img src="assets/print_flow.png" alt="Print Flow Diagram">'
            )

        # TRANSFORM MARKDOWN TO HTML
        if not is_html:
            import markdown
            self.content_text = markdown.markdown(
                self.content_text,
                extensions=['fenced_code', 'tables']
            )

        # UNIFIED RENDERER
        from utils.html_renderer import render_html
        rendered_content = render_html(self.content_text, theme=self.theme)
        content_column.controls.append(rendered_content)
        
        # Set container properties AFTER super().__init__()
        self.content = content_column
        self.padding = 40
        self.bgcolor = bg_color
        self.expand = True
        self.border_radius = 10
