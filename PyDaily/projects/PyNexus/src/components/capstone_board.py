"""
Capstone Board Component - Kanban board for Capstone project stories.
Replaces the placeholder TicketBoard.
"""
import flet as ft
from pathlib import Path
from components.capstone_card import build_capstone_card
from services.capstone_service import CapstoneService
from services.scaffolder import Scaffolder
from services.progress_tracker import ProgressTracker


class CapstoneBoard(ft.Container):
    """Kanban board for Capstone project stories."""
    
    COLUMNS = [
        {"key": "backlog", "title": "BACKLOG", "colors": ["#2d3436", "#000000"]},
        {"key": "in_progress", "title": "IN PROGRESS", "colors": ["#0f2027", "#203a43"]},
        {"key": "shipped", "title": "SHIPPED", "colors": ["#134e5e", "#71b280"]},
    ]
    
    def __init__(self, page: ft.Page, phase: int = 1):
        super().__init__()
        self.app_page = page
        self.phase = phase
        self.expand = True
        
        # Services
        self.capstone_service = CapstoneService()
        self.scaffolder = Scaffolder()
        self.progress = ProgressTracker()
        
        # Data
        self.project = None
        self.stories = []
        
        # UI references
        self.column_containers = {}
        self.current_dialog = None
        
        # Custom Overlay for Results
        self.results_overlay = ft.Container(
            visible=False,
            bgcolor=ft.Colors.with_opacity(0.8, "#000000"),
            alignment=ft.Alignment(0, 0),
            on_click=None, # Blocking click
            expand=True,

        )
        
        # Build initial UI
        self._build_board()
    
    def did_mount(self):
        """Called when component is mounted - load data."""
        self.load_stories()
    
    def load_stories(self):
        """Load stories for the current phase."""
        print(f"DEBUG: Loading stories for Phase {self.phase}...")
        self.project, self.stories = self.capstone_service.get_stories_for_phase(self.phase)
        
        if self.project:
            print(f"DEBUG: Loaded project: {self.project.get('project_title')}")
            print(f"DEBUG: Loaded {len(self.stories)} stories")
        else:
            print(f"DEBUG: No project found for Phase {self.phase}")
        
        # Assign status to each story based on local progress
        for story in self.stories:
            story_id = str(story.get('id', ''))
            if self.progress.is_completed(story_id):
                story['status'] = 'shipped'
            elif self.progress.is_in_progress(story_id):
                story['status'] = 'in_progress'
            else:
                story['status'] = 'backlog'
        
        self.update_board()
    
    def set_phase(self, phase: int):
        """Change the current phase and reload stories."""
        self.phase = phase
        self.load_stories()
    
    def update_board(self):
        """Update all column contents based on current story statuses."""
        # Group stories by status
        grouped = {col['key']: [] for col in self.COLUMNS}
        
        for story in self.stories:
            status = story.get('status', 'backlog')
            if status in grouped:
                grouped[status].append(story)
        
        # Rebuild each column
        for col in self.COLUMNS:
            key = col['key']
            if key in self.column_containers:
                container = self.column_containers[key]
                container.controls.clear()
                
                for story in grouped[key]:
                    story_id = str(story.get('id', ''))
                    retries = self.progress.get_retries(story_id)
                    card = build_capstone_card(
                        story=story,
                        status=key,
                        on_start=self.start_story,
                        on_test=self.test_story,
                        on_continue=self.continue_story,
                        retries=retries
                    )
                    container.controls.append(card)
                
                print(f"DEBUG: Column {key} has {len(grouped[key])} stories")
        
        if self.app_page:
            self.app_page.update()
    
    def _build_board(self):
        """Build the initial board structure."""
        columns = []
        
        for col in self.COLUMNS:
            # Create scrollable container for cards
            cards_column = ft.Column([], spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
            self.column_containers[col['key']] = cards_column
            
            column_container = ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=ft.Text(col['title'], weight="bold", size=12, color=ft.Colors.WHITE_70),
                        padding=ft.Padding(0, 0, 0, 10),
                        bgcolor=ft.Colors.with_opacity(0.3, "#1e293b"),
                        border_radius=ft.BorderRadius.only(top_left=10, top_right=10)
                    ),
                    # Cards
                    ft.Container(
                        content=cards_column,
                        expand=True,
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(0.2, "#1e293b"),
                        border_radius=ft.BorderRadius.only(bottom_left=10, bottom_right=10)
                    ),
                ], spacing=0, expand=True),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1),
                    colors=[ft.Colors.with_opacity(0.8, c) for c in col['colors']]
                ),
                padding=10,
                border_radius=12,
                expand=True,
                border=ft.Border.all(1, ft.Colors.WHITE_10),
            )
            columns.append(column_container)
        
        board_row = ft.Row(columns, spacing=16, expand=True, alignment=ft.MainAxisAlignment.START)
        
        self.content = ft.Stack([
            board_row,
            self.results_overlay
        ], expand=True)
    
    def _convert_story_to_exercise(self, story: dict) -> dict:
        """Convert story format to exercise format for Scaffolder compatibility."""
        # Build comprehensive instructions from story data
        instructions = f"{story.get('description', '')}"
        
        # Add acceptance criteria
        criteria = story.get('acceptance_criteria', [])
        if criteria:
            instructions += "\n\n## Acceptance Criteria\n"
            for c in criteria:
                instructions += f"- {c}\n"
        
        # Add hints
        hints = story.get('hints', [])
        if hints:
            instructions += "\n## Hints\n"
            for h in hints:
                instructions += f"- {h}\n"
        
        return {
            'id': story.get('id'),
            'day_number': 0,  # Capstone projects don't have day numbers
            'difficulty': f"Phase{self.phase}",
            'title': story.get('story_code', 'Story'),
            'starter_code': story.get('starter_code', ''),
            'test_code': story.get('test_code', ''),
            'xp': story.get('xp', 15),
            'instructions': instructions,
        }
    
    def start_story(self, story: dict):
        """Start a new story: scaffold files and open VS Code."""
        try:
            story_id = str(story.get('id', ''))
            exercise = self._convert_story_to_exercise(story)
            
            # Scaffold the exercise
            path = self.scaffolder.scaffold_exercise(exercise)
            success, msg = self.scaffolder.launch_vscode(path)
            
            # Track progress
            self.progress.mark_in_progress(story_id)
            story['status'] = 'in_progress'
            
            self.update_board()
            
            self.app_page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="#1e293b")
            self.app_page.snack_bar.open = True
            self.app_page.update()
            
        except Exception as e:
            self.app_page.snack_bar = ft.SnackBar(ft.Text(f"Failed to start: {e}"), bgcolor="#dc2626")
            self.app_page.snack_bar.open = True
            self.app_page.update()
    
    def continue_story(self, story: dict):
        """Re-open VS Code for an in-progress story."""
        try:
            exercise = self._convert_story_to_exercise(story)
            path = self.scaffolder.get_exercise_path(exercise)
            
            if not path.exists():
                path = self.scaffolder.scaffold_exercise(exercise)
            
            success, msg = self.scaffolder.launch_vscode(path)
            self.app_page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="#1e293b")
            self.app_page.snack_bar.open = True
            self.app_page.update()
            
        except Exception as e:
            self.app_page.snack_bar = ft.SnackBar(ft.Text(f"Failed to open: {e}"), bgcolor="#dc2626")
        self.app_page.snack_bar.open = True
        self.app_page.update()
    
    def test_story(self, story: dict):
        """Run pytest on the story and show results."""
        print(f"DEBUG: test_story called for {story.get('story_code')}")
        
        # Hide overlay just in case
        self.results_overlay.visible = False
        self.results_overlay.update()
        
        try:
            story_id = str(story.get('id', ''))
            xp = story.get('xp', 15)
            exercise = self._convert_story_to_exercise(story)
            path = self.scaffolder.get_exercise_path(exercise)
            
            if not path.exists():
                self.app_page.snack_bar = ft.SnackBar(
                    ft.Text(f"Story folder not found at {path}! Click folder icon to open."),
                    bgcolor="#dc2626"
                )
                self.app_page.snack_bar.open = True
                self.app_page.update()
                return
            
            # Re-scaffold to ensure test file is properly formatted
            self.scaffolder.scaffold_exercise(exercise)
            
            # Run pytest
            print(f"DEBUG: Running tests for {path}")
            passed, output, stats = self.scaffolder.run_tests(path)
            print(f"DEBUG: Test finished. Passed: {passed}")
            
            if passed:
                self.progress.add_xp(story_id, xp)
                story['status'] = 'shipped'
                self.update_board()
            else:
                self.progress.increment_retry(story_id)

            # --- Result Display Logic (Stack Overlay) ---
            retries = self.progress.get_retries(story_id)
            
            # Header
            header = None
            if passed:
                header = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400, size=32),
                        ft.Column([
                            ft.Text("TESTS PASSED!", size=20, weight="bold", color=ft.Colors.GREEN_400),
                            ft.Text(f"+ {xp} XP Earned", size=14, color=ft.Colors.GREY_400)
                        ], spacing=2)
                    ], spacing=12),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.GREEN_400),
                    border_radius=8
                )
            else:
                header = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_400, size=32),
                        ft.Column([
                            ft.Text("TESTS FAILED", size=20, weight="bold", color=ft.Colors.RED_400),
                            ft.Text(f"Attempt #{retries} - Keep trying!", size=14, color=ft.Colors.GREY_400)
                        ], spacing=2)
                    ], spacing=12),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.RED_400),
                    border_radius=8
                )
            
            # Hints
            hints = story.get('hints', [])
            hint_section = []
            if not passed and hints:
                hint_text = "\n".join([f"💡 {h}" for h in hints])
                hint_section = [
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Text(hint_text, size=12, color=ft.Colors.AMBER_300),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.AMBER_400),
                        padding=12,
                        border_radius=6,
                    )
                ]
            
            display_output = output if len(output) < 1500 else output[:1500] + "\n\n... (truncated)"
            
            # Build Content Card
            content_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Test Results: {story.get('story_code', '')}", size=16, weight="bold"),
                        ft.IconButton(ft.Icons.CLOSE, on_click=self._handle_close)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(color=ft.Colors.WHITE_10),
                    ft.Column([
                        header,
                        *hint_section,
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Text(display_output, size=11, font_family="Consolas"),
                            bgcolor="#0f172a",
                            padding=12,
                            border_radius=8,
                            expand=True,
                        )
                    ], scroll=ft.ScrollMode.AUTO, expand=True),
                    ft.Row([
                        ft.ElevatedButton("Close", on_click=self._handle_close, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.END)
                ], spacing=10),
                bgcolor="#1e293b",
                padding=25,
                border_radius=16,
                width=600,
                height=550,
                border=ft.Border.all(1, ft.Colors.WHITE_10),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=20,
                    color=ft.Colors.BLACK,
                    offset=ft.Offset(0, 4)
                )
            )
            
            # Show In Overlay
            self.results_overlay.content = content_card
            self.results_overlay.visible = True
            self.results_overlay.update()
            
        except Exception as e:
            print(f"Error testing story: {e}")
            self.app_page.snack_bar = ft.SnackBar(ft.Text(f"Error: {e}"), bgcolor="#dc2626")
            self.app_page.snack_bar.open = True
            self.app_page.update()
    
    def _handle_close(self, e):
        """Close the results overlay."""
        print("CLOSE: Hiding overlay")
        self.results_overlay.visible = False
        self.results_overlay.content = None
        self.results_overlay.update()
