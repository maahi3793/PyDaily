import flet as ft
from services.content_manager import ContentManager
from components.reader_view import ReaderView

class LibraryView(ft.Container):
    def __init__(self, page: ft.Page, use_sidebar=True):
        super().__init__()
        self.app_page = page
        self.expand = True
        self.content_manager = ContentManager()
        self.timeline_data = {}
        self.selected_day = None
        
        # UI Components
        self.sidebar_content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.main_content_area = ft.Container(
            expand=True, 
            padding=20,
            bgcolor="#0f172a",
            content=ft.Column([
                ft.Container(height=100),
                ft.Row([
                    ft.Icon(ft.Icons.LIBRARY_BOOKS, size=40, color=ft.Colors.BLUE_300),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Select a day from the archive", size=16, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        )
        
        # Use cached data if available
        try:
            from main import data_cache
            cached_timeline = data_cache.get_timeline()
            if cached_timeline:
                print("DEBUG: Using cached timeline data")
                self.timeline_data = cached_timeline
                self.populate_sidebar()
            else:
                print("DEBUG: Loading timeline data...")
                self._load_data_async()
        except ImportError:
            print("DEBUG: Cache not available, loading fresh data")
            self._load_data_async()
        
        # Content sidebar styling
        content_sidebar = ft.Container(
            width=260,
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.ARCHIVE, color=ft.Colors.BLUE_400, size=18),
                            ft.Text("NEXUS ARCHIVES", size=14, weight="bold", color=ft.Colors.BLUE_300),
                        ], spacing=8),
                    ], spacing=10),
                    padding=ft.Padding(16, 20, 16, 10),
                ),
                ft.Divider(color="#334155", height=1),
                self.sidebar_content,
            ], expand=True),
            bgcolor="#1e293b",
            border=ft.Border(right=ft.BorderSide(1, "#334155")),
        )

        # Main layout
        main_layout = ft.Row([
            content_sidebar,
            self.main_content_area
        ], spacing=0, expand=True)

        if use_sidebar:
            from components.sidebar import Sidebar
            self.content = ft.Row([
                Sidebar(page, selected_index=1),
                main_layout
            ], spacing=0, expand=True)
        else:
            self.content = main_layout
    
    def _load_data_async(self):
        """Load timeline data (with caching)."""
        try:
            self.timeline_data = self.content_manager.get_timeline_data()
            try:
                from main import data_cache
                data_cache.set_timeline(self.timeline_data)
            except ImportError:
                pass
            self.populate_sidebar()
        except Exception as e:
            print(f"ERROR: LibraryView data load failed: {e}")
            # Do not wipe data if it was partially loaded or if UI update failed
            if not self.timeline_data:
                self.timeline_data = {}

    def populate_sidebar(self):
        self.sidebar_content.controls.clear()
        
        sorted_days = sorted(self.timeline_data.keys())
        valid_days = [d for d in sorted_days if self.timeline_data[d].get('title') and "Unlocked" not in self.timeline_data[d].get('title', '')]
        
        for day in valid_days:
            topic_title = self.timeline_data[day].get('title', f"Day {day}")
            is_selected = self.selected_day == day
            
            tile = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"DAY {day}", size=10, color=ft.Colors.BLUE_400 if is_selected else ft.Colors.GREY_500, weight="bold"),
                        ft.Text(topic_title, weight="bold", size=12, color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400, 
                               overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
                    ], spacing=2, expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, size=14, color=ft.Colors.BLUE_400 if is_selected else ft.Colors.TRANSPARENT),
                ]),
                padding=ft.Padding(14, 10, 14, 10),
                border_radius=8,
                ink=True,
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_400) if is_selected else ft.Colors.TRANSPARENT,
                border=ft.Border.all(1, ft.Colors.BLUE_600 if is_selected else ft.Colors.TRANSPARENT),
            )
            tile.on_click = lambda e, d=day: self.load_day_content(d)
            self.sidebar_content.controls.append(tile)
        
        # Safely update UI
        try:
            if hasattr(self, 'app_page') and hasattr(self.sidebar_content, 'page') and self.sidebar_content.page:
                self.sidebar_content.update()
        except Exception as e:
             # Ignore UI update errors during init (control not added to page yet)
             pass


    def _render_quiz_as_markdown(self, quiz_data, day):
        """Convert JSON quiz data to readable Markdown format."""
        lines = [f"# Day {day} Checkpoint Quiz\n"]
        lines.append("Test your knowledge with the following questions:\n\n---\n")
        
        if isinstance(quiz_data, dict):
            title = quiz_data.get('title', f'Day {day} Quiz')
            questions = quiz_data.get('questions', [])
            lines[0] = f"# {title}\n"
        elif isinstance(quiz_data, list):
            questions = quiz_data
        else:
            return f"# Day {day} Quiz\n\n*Invalid quiz data format.*"
        
        for i, q in enumerate(questions, 1):
            question_text = q.get('question', 'No question text')
            options = q.get('options', [])
            answer = q.get('answer', '')
            explanation = q.get('explanation', '')
            
            lines.append(f"## Question {i}\n")
            lines.append(f"{question_text}\n\n")
            
            if options:
                for opt in options:
                    lines.append(f"- {opt}\n")
                lines.append("\n")
            
            if answer:
                lines.append(f"**Answer:** {answer}\n\n")
            if explanation:
                lines.append(f"*{explanation}*\n\n")
            
            lines.append("---\n\n")
        
        return "".join(lines)

    def load_day_content(self, day):
        self.selected_day = day
        self.populate_sidebar()
        
        # Check cache first
        try:
            from main import data_cache
            cache_key = f"day_{day}_content"
            cached = data_cache.get(cache_key)
        except ImportError:
            cached = None
        
        if cached:
            print(f"DEBUG: Using cached content for Day {day}")
            data = cached
        else:
            print(f"DEBUG: Loading content for Day {day}")
            data = self.content_manager.get_day_content(day)
            try:
                from main import data_cache
                data_cache.set(f"day_{day}_content", data)
            except ImportError:
                pass
        
        topic_text = data.get('topic_content') or ''
        
        # Quiz detection
        if topic_text and (topic_text.strip().startswith('{') or topic_text.strip().startswith('[')):
            import json
            try:
                quiz_data = json.loads(topic_text)
                topic_text = self._render_quiz_as_markdown(quiz_data, day)
            except json.JSONDecodeError:
                pass
        
        if not topic_text:
            topic_text = '# No Topic Available\n\nCheck database connection.'

        chap = data.get('chapter', {})
        theory_content = chap.get('content_part1_theory') or '# No Theory Content'
        practice_content = chap.get('content_part2_practice') or '# No Practice Content'
        mentor_content = chap.get('content_part3_mentor') or '# Mentor is offline.\n\n*Proceed with the mission, Agent.*'

        # Image placeholders
        import re
        image_map = {}
        search_text = (theory_content or "") + (topic_text or "")
        placeholders = re.findall(r'<!-- IMAGE_PLACEHOLDER: (.*?) -->', search_text)
        if placeholders:
            image_map = self.content_manager.get_image_urls(placeholders)

        if 'battle' in data:
            brief = data['battle'].get('mission_brief', '')
            practice_content += f"\n\n---\n\n## ⚔️ BOSS BATTLE PROTOCOL\n\n{brief}"

        # Create views
        view_briefing = ReaderView(topic_text, title=f"Day {day}: Topic", theme="dark", image_map=image_map)
        view_theory = ReaderView(theory_content, title=f"Day {day}: Deep Dive", theme="dark", image_map=image_map)
        view_practice = ft.Column([
            ReaderView(practice_content, title=f"Day {day}: Practice Protocol", theme="dark", image_map=image_map),
        ], scroll=ft.ScrollMode.ALWAYS)
        view_mentor = ReaderView(mentor_content, title=f"Day {day}: Mentor Log", theme="dark", image_map=image_map)
        
        views_list = [view_briefing, view_theory, view_practice, view_mentor]

        # Modern tabs with blue theme
        t1, t2, t3, t4 = ft.Tab(), ft.Tab(), ft.Tab(), ft.Tab()
        t1.text, t1.icon = "TOPIC", ft.Icons.LIGHTBULB_OUTLINED
        t2.text, t2.icon = "THEORY", ft.Icons.BOOK_OUTLINED
        t3.text, t3.icon = "PRACTICE", ft.Icons.CODE_OUTLINED
        t4.text, t4.icon = "MENTOR", ft.Icons.PSYCHOLOGY_OUTLINED

        tab_bar = ft.TabBar(
            tabs=[t1, t2, t3, t4],
            divider_color="#334155",
            indicator_color=ft.Colors.BLUE_400,
            label_color=ft.Colors.BLUE_200,
            unselected_label_color=ft.Colors.GREY_500,
        )

        tab_view = ft.TabBarView(controls=views_list)

        tabs_controller = ft.Tabs(
            selected_index=0,
            length=4,
            animation_duration=200,
            content=ft.Column([
                tab_bar,
                ft.Divider(height=1, color="#334155"),
                ft.Container(content=tab_view, expand=True)
            ], expand=True, spacing=0),
            expand=True
        )

        self.main_content_area.content = tabs_controller
        self.main_content_area.update()
