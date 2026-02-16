from services.auth import AuthService
from services.scaffolder import Scaffolder
from services.progress_tracker import ProgressTracker
import flet as ft
from pathlib import Path

class KanbanBoard(ft.Container):
    def __init__(self, page: ft.Page, use_sidebar=True):
        super().__init__()
        self.app_page = page
        self.expand = True
        self.padding = 0 
        self.use_sidebar = use_sidebar
        
        # Services
        self.auth = AuthService()
        self.scaffolder = Scaffolder()
        self.progress = ProgressTracker()
        self.exercises = [] 

        # Board Config - Modern Colors
        self.columns = [
            {"title": "TO DO", "id": "todo", "color": "#7c3aed", "accent": "#a78bfa"},
            {"title": "IN PROGRESS", "id": "in_progress", "color": "#2563eb", "accent": ft.Colors.BLUE_400},
            {"title": "COMPLETE", "id": "done", "color": "#16a34a", "accent": ft.Colors.GREEN_400},
        ]
        
        # Initialize Overlay (Hidden by default)
        self.results_overlay = ft.Container(
            visible=False,
            bgcolor=ft.Colors.with_opacity(0.8, "#000000"),
            alignment=ft.Alignment(0, 0),
            on_click=None, # Blocking click
            expand=True,
        )

        main_content = self.build_main_content()
        
        layout = main_content
        if use_sidebar:
            from components.sidebar import Sidebar
            layout = ft.Row([
                Sidebar(page, selected_index=2),
                main_content
            ], spacing=0, expand=True)

        # Wrap in Stack to support overlay
        self.content = ft.Stack([
            layout,
            self.results_overlay
        ], expand=True)

    def did_mount(self):
        self.load_exercises(day=1)
    
    def on_day_change(self, e):
        """Handle day dropdown change - loads exercises for selected day."""
        day = int(e.control.value)
        print(f"DEBUG: on_day_change triggered with day={day}")
        self.load_exercises(day)
        print(f"DEBUG: on_day_change calling self.update()")
        self.update()
    
    def on_difficulty_change(self, e):
        """Handle difficulty dropdown change - filters board immediately."""
        print(f"DEBUG: on_difficulty_change triggered with value={e.control.value}")
        self.update_board()
        print(f"DEBUG: on_difficulty_change calling self.update()")
        self.update()

    def build_main_content(self):
        self.day_picker = ft.Dropdown(
            width=130,
            options=[ft.dropdown.Option(str(i), f"Day {i}") for i in range(1, 31)],
            value="1",
            label="Day",
            border_color="#334155",
            focused_border_color=ft.Colors.BLUE_400,
        )
        self.day_picker.on_change = self.on_day_change
        
        self.difficulty_filter = ft.Dropdown(
            width=150,
            options=[
                ft.dropdown.Option("All", "All Levels"),
                ft.dropdown.Option("Easy", "Easy (XP 10)"),
                ft.dropdown.Option("Medium", "Medium (XP 20)"),
                ft.dropdown.Option("Hard", "Hard (XP 30)"),
                ft.dropdown.Option("Scenario", "Boss Battle"),
            ],
            value="All",
            label="Difficulty",
            border_color="#334155",
            focused_border_color=ft.Colors.BLUE_400,
        )
        self.difficulty_filter.on_change = self.on_difficulty_change

        self.cols_row = ft.Row([
            self.build_column(col) for col in self.columns
        ], expand=True, spacing=16, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
        
        self.header_title = ft.Text(
            "MISSION CONTROL (DAY 1)", 
            size=22, weight="bold", 
            color=ft.Colors.BLUE_300
        )

        return ft.Container(
            content=ft.Column([
                # Header Row
                ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.VIEW_KANBAN, color=ft.Colors.BLUE_400, size=24),
                        self.header_title,
                    ], spacing=10),
                    ft.Row([
                        self.day_picker, 
                        self.difficulty_filter,
                        ft.ElevatedButton(
                            "GO",
                            icon=ft.Icons.ARROW_FORWARD,
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            on_click=lambda _: self.load_exercises(int(self.day_picker.value))
                        )
                    ], spacing=8)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Divider(color="#334155"),
                self.cols_row
            ], spacing=16),
            padding=30,
            expand=True,
            bgcolor="#0f172a"
        )

    def load_exercises(self, day):
        if not self.auth.client:
            self.app_page.snack_bar = ft.SnackBar(ft.Text("Database disconnected"), bgcolor="#1e293b")
            self.app_page.snack_bar.open = True
            return

        try:
            self.header_title.value = f"MISSION CONTROL (DAY {day})"
            
            print(f"DEBUG: Loading Day {day}...")
            res = self.auth.client.table("exercises").select("*").eq("day_number", day).execute()
            self.exercises = res.data
            
            for ex in self.exercises:
                ex_id = str(ex.get('id', ''))
                title = self.scaffolder.sanitize_name(ex.get('title', 'Untitled'))
                diff = ex.get('difficulty', 'Easy')
                path = self.scaffolder.practice_root / f"Day_{day:02d}" / f"{diff}_{title}"
                
                # Check completion status from local progress
                if self.progress.is_completed(ex_id):
                    ex['status'] = 'done'
                elif path.exists() or self.progress.is_in_progress(ex_id):
                    ex['status'] = 'in_progress'
                else:
                    ex['status'] = 'todo'
            
            print(f"DEBUG: Day {day} loaded. Count: {len(self.exercises)}")
            self.update_board()
            
            if self.page:
                self.app_page.update()
            
        except Exception as e:
            print(f"Error loading exercises: {e}")
            import traceback
            traceback.print_exc()

    def update_board(self, e=None):
        target_diff = self.difficulty_filter.value
        print(f"DEBUG: Filtering by {target_diff}")
        
        for i, col_meta in enumerate(self.columns):
            task_list_container = self.cols_row.controls[i].content.controls[1]
            col_id = col_meta['id']
            
            col_exs = []
            for ex in self.exercises:
                ex_status = ex.get('status', 'todo')
                ex_diff = ex.get('difficulty', 'Unknown')
                
                if ex_status != col_id:
                    continue
                    
                if target_diff != "All" and ex_diff != target_diff:
                    continue
                    
                col_exs.append(ex)

            print(f"DEBUG: Column {col_id} has {len(col_exs)} items")
            task_list_container.content.controls = [self.build_task_card(ex, col_meta['accent']) for ex in col_exs]
            
            # Update the inner container
            if task_list_container.page:
                task_list_container.update()
        
        # Force full page update to ensure UI refreshes
        if self.app_page:
            self.app_page.update()

    def build_column(self, col_data):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Container(width=4, height=16, bgcolor=col_data["accent"], border_radius=2),
                        ft.Text(col_data["title"], weight="bold", color=ft.Colors.WHITE, size=13),
                    ], spacing=8),
                    padding=12,
                    bgcolor=col_data["color"],
                    border_radius=ft.border_radius.only(top_left=10, top_right=10)
                ),
                ft.Container(
                    content=ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO),
                    padding=12,
                    bgcolor="#1e293b",
                    expand=True, 
                    border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
                )
            ]),
            border_radius=10,
            border=ft.Border.all(1, "#334155"),
            expand=True
        )

    def build_task_card(self, task, accent_color):
        difficulty = task.get("difficulty", "Normal")
        status = task.get("status", "todo")
        ex_id = str(task.get('id', ''))
        xp = task.get('xp', 10)
        
        diff_colors = {
            "Easy": ft.Colors.GREEN_700,
            "Medium": ft.Colors.AMBER_700,
            "Hard": ft.Colors.RED_700,
            "Scenario": "#6d28d9",
        }
        
        # Retry-based border color (more retries = redder border)
        retries = self.progress.get_retries(ex_id)
        border_color = "#334155"  # default
        if retries == 1:
            border_color = "#7c3aed"  # purple hint
        elif retries == 2:
            border_color = "#dc2626"  # red
        elif retries >= 3:
            border_color = "#b91c1c"  # dark red
        
        # Build buttons based on status
        if status == "todo":
            buttons = ft.Row([
                ft.ElevatedButton(
                    "START MISSION",
                    icon=ft.Icons.ROCKET_LAUNCH,
                    color=ft.Colors.WHITE,
                    bgcolor=accent_color,
                    on_click=lambda e, t=task: self.launch_mission(t)
                )
            ])
        elif status == "in_progress":
            buttons = ft.Row([
                ft.ElevatedButton(
                    "TEST",
                    icon=ft.Icons.SCIENCE,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.GREEN_700,
                    on_click=lambda e, t=task: self.test_solution(t)
                ),
                ft.IconButton(
                    ft.Icons.FOLDER_OPEN,
                    icon_color=ft.Colors.BLUE_400,
                    tooltip="Continue in VS Code",
                    on_click=lambda e, t=task: self.continue_mission(t)
                )
            ], spacing=4)
        else:  # done
            buttons = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400, size=16),
                    ft.Text(f"+{xp} XP", color=ft.Colors.GREEN_400, weight="bold", size=12)
                ], spacing=4),
                padding=ft.Padding(8, 4, 8, 4),
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.GREEN_400),
                border_radius=4
            )
        
        # Hint for struggling users (3+ retries)
        hint_text = None
        if retries >= 3 and status == "in_progress":
            hint_text = ft.Text(
                "💡 Need help? Review the lesson!",
                size=10, color=ft.Colors.AMBER_300, italic=True
            )
        
        card_content = [
            ft.Text(task.get("title", "?"), color=ft.Colors.WHITE, weight="bold", size=14),
            ft.Container(height=6),
            ft.Row([
                ft.Container(
                    content=ft.Text(difficulty, size=10, color=ft.Colors.WHITE, weight="bold"),
                    bgcolor=diff_colors.get(difficulty, ft.Colors.BLUE_GREY_700),
                    padding=ft.Padding(8, 4, 8, 4),
                    border_radius=4
                ),
                ft.Text(f"XP: {xp}", size=11, color=ft.Colors.AMBER_300, weight="bold")
            ], spacing=8),
            ft.Container(height=10),
            buttons
        ]
        
        if hint_text:
            card_content.insert(-1, hint_text)
        
        card = ft.Container(
            content=ft.Column(card_content),
            padding=14,
            bgcolor="#0f172a",
            border_radius=8,
            border=ft.Border.all(2 if retries >= 2 else 1, border_color)
        )
        return card

    def launch_mission(self, task):
        """Start a new mission: scaffold files, open VS Code, mark in progress."""
        try:
            ex_id = str(task.get('id', ''))
            path = self.scaffolder.scaffold_exercise(task)
            success, msg = self.scaffolder.launch_vscode(path)
            
            # Track in local progress
            self.progress.mark_in_progress(ex_id)
            
            task['status'] = 'in_progress'
            self.update_board()
            self.app_page.update()
            
            self.app_page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="#1e293b")
            self.app_page.snack_bar.open = True
            
        except Exception as e:
            self.app_page.snack_bar = ft.SnackBar(ft.Text(f"Launch Failed: {e}"), bgcolor="#7c3aed")
            self.app_page.snack_bar.open = True
            self.app_page.update()
    
    def continue_mission(self, task):
        """Re-open VS Code for an in-progress mission."""
        try:
            path = self.scaffolder.get_exercise_path(task)
            if not path.exists():
                # Folder was deleted, re-scaffold
                path = self.scaffolder.scaffold_exercise(task)
            
            success, msg = self.scaffolder.launch_vscode(path)
            self.app_page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="#1e293b")
            self.app_page.snack_bar.open = True
            self.app_page.update()
            
        except Exception as e:
            self.app_page.snack_bar = ft.SnackBar(ft.Text(f"Failed to open: {e}"), bgcolor="#7c3aed")
            self.app_page.snack_bar.open = True
            self.app_page.update()
    
    def test_solution(self, task):
        """Run pytest on the exercise and show results in a custom overlay."""
        try:
            ex_id = str(task.get('id', ''))
            xp = task.get('xp', 10)
            path = self.scaffolder.get_exercise_path(task)
            
            print(f"DEBUG: test_solution called for task: {task.get('title')}")
            
            # Hide overlay just in case
            self.results_overlay.visible = False
            self.results_overlay.update()

            if not path.exists():
                self.app_page.snack_bar = ft.SnackBar(
                    ft.Text("Exercise folder not found! Click folder icon to re-open."), 
                    bgcolor="#dc2626"
                )
                self.app_page.snack_bar.open = True
                self.app_page.update()
                return
            
            # Re-scaffold to ensure test file is properly formatted
            print(f"DEBUG: Re-scaffolding exercise to update test file...")
            self.scaffolder.scaffold_exercise(task)
            
            # Run pytest
            print(f"DEBUG: About to run pytest...")
            passed, output, stats = self.scaffolder.run_tests(path)
            print(f"DEBUG: pytest result - passed: {passed}")
            
            if passed:
                # SUCCESS! Add XP and mark complete
                self.progress.add_xp(ex_id, xp)
                self.progress.reset_retries(ex_id)
                task['status'] = 'done'
            else:
                # FAILED - increment retry and show errors
                self.progress.increment_retry(ex_id)
            
            # Show Results in Stack Overlay
            self.show_results_overlay(passed, output, task, xp)
            
            self.update_board()
            self.app_page.update()
            
        except Exception as e:
            print(f"DEBUG: Exception in test_solution: {e}")
            import traceback
            traceback.print_exc()
            self.app_page.snack_bar = ft.SnackBar(ft.Text(f"Test Error: {e}"), bgcolor="#dc2626")
            self.app_page.snack_bar.open = True
            self.app_page.update()
    
    def show_results_overlay(self, passed: bool, output: str, task: dict, xp: int):
        """Show pytest results in the custom Stack overlay."""
        ex_id = str(task.get('id', ''))
        retries = self.progress.get_retries(ex_id)
        
        if passed:
            header = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CELEBRATION, color=ft.Colors.AMBER_400, size=32),
                    ft.Column([
                        ft.Text("MISSION COMPLETE!", size=20, weight="bold", color=ft.Colors.GREEN_400),
                        ft.Text(f"+{xp} XP earned!", size=14, color=ft.Colors.AMBER_300)
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
        
        # Truncate output if too long
        display_output = output if len(output) < 2000 else output[:2000] + "\n\n... (output truncated)"
        
        # Build Content Card for Overlay
        content_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"Test Results: {task.get('title', 'Exercise')}", size=16, weight="bold"),
                    ft.IconButton(ft.Icons.CLOSE, on_click=self.handle_close)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color=ft.Colors.WHITE_10),
                ft.Column([
                    header,
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
                    ft.ElevatedButton("Close", on_click=self.handle_close, color=ft.Colors.WHITE)
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
        
        self.results_overlay.content = content_card
        self.results_overlay.visible = True
        self.results_overlay.update()
    
    def handle_close(self, e):
        """Handle close button click."""
        print("DEBUG: Closing overlay")
        self.results_overlay.visible = False
        self.results_overlay.content = None
        self.results_overlay.update()
