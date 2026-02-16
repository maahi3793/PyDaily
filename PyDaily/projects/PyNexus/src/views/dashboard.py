"""
Dashboard View - Capstone Projects.
Focuses on the long-term project board.
"""
import flet as ft
from components.capstone_board import CapstoneBoard
from services.capstone_service import CapstoneService

PHASE_GOALS = {
    1: "Getting comfortable with syntax and basic logic.",
    2: "Writing reusable code and handling data.",
    3: "Structuring code using Classes and Objects.",
    4: "Computer Science fundamentals for interviews and optimization.",
    5: "Mastering the 'Pythonic' way and internal mechanics.",
    6: "Concurrency, Architecture, and Professional Practices."
}

class DashboardView(ft.Container):
    def __init__(self, page: ft.Page, use_sidebar=True):
        super().__init__()
        self.app_page = page
        self.expand = True
        self.current_phase = 1
        
        # Services
        self.capstone_service = CapstoneService()
        
        # Initial Data Fetch
        self.project = self.capstone_service.get_project_for_phase(self.current_phase)
        
        # --- UI COMPONENTS ---
        self.project_area = self.build_project_area()
        self.capstone_board = CapstoneBoard(page, phase=self.current_phase)

        # Main Layout
        main_content = ft.Container(
            content=ft.Column([
                self.project_area,
                ft.Container(height=10),
                self.capstone_board,
            ], expand=True, spacing=0), # SCROLL REMOVED to fix layout!
            padding=20,
            expand=True,
            bgcolor="#0f172a" 
        )

        if use_sidebar:
            from components.sidebar import Sidebar
            self.content = ft.Row([
                Sidebar(page, selected_index=1),
                main_content
            ], spacing=0, expand=True)
        else:
            self.content = main_content
    
    def build_project_area(self):
        """Builds the Phase Selector and Project Card."""
        # Phase dropdown
        self.phase_dropdown = ft.Dropdown(
            value=str(self.current_phase),
            options=[ft.dropdown.Option(str(i), f"Phase {i}") for i in range(1, 7)],
            width=140,
            text_size=12,
            height=36,
            bgcolor="#0f172a",
            border_color=ft.Colors.BLUE_400,
            content_padding=10,
        )
        self.phase_dropdown.on_change = lambda _: self.on_phase_change(None)
        
        self.project_title = ft.Text(
            self.project.get('project_title', 'No Project') if self.project else 'No Project for this Phase',
            size=18, weight="bold", color=ft.Colors.WHITE
        )
        self.project_goal = ft.Text(
            PHASE_GOALS.get(self.current_phase, ''),
            size=13, color=ft.Colors.GREY_400, italic=True
        )

        return ft.Container(
            content=ft.Column([
                # Header Row
                ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.DASHBOARD, color=ft.Colors.BLUE_400, size=24),
                        ft.Text("CAPSTONE PROJECT", size=20, weight="bold", color=ft.Colors.BLUE_300),
                    ], spacing=10),
                    self.phase_dropdown
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Divider(color=ft.Colors.WHITE_10, height=20),
                
                # Project Info
                ft.Row([
                    ft.Column([
                        self.project_title,
                        self.project_goal,
                    ], expand=True),
                    
                    ft.ElevatedButton(
                        "Set Phase", # Renamed back to Set Phase
                        icon=ft.Icons.CHECK, # Changed icon to check? Or Refresh? User said "Set Phase Button". 
                        # Original image likely had "Set Phase" text.
                        # I'll keep Check or Refresh. Check implies "Commit".
                        # Previous code used Refresh. I'll use Check for "Set".
                        icon_color=ft.Colors.BLUE_200,
                        color=ft.Colors.BLUE_100,
                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_900),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        height=36,
                        on_click=lambda _: self.on_phase_change(None) 
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                
            ]),
            padding=25,
            bgcolor=ft.Colors.with_opacity(0.4, "#1e293b"),
            border=ft.Border.all(1, ft.Colors.WHITE_10),
            border_radius=12,
        )

    def on_phase_change(self, e):
        """Handle phase dropdown change."""
        try:
            new_phase = int(self.phase_dropdown.value)
            self.current_phase = new_phase
            
            # Update project info
            self.project = self.capstone_service.get_project_for_phase(new_phase)
            
            if self.project:
                self.project_title.value = self.project.get('project_title', 'No Project')
            else:
                self.project_title.value = f"Phase {new_phase} - Coming Soon"
            
            self.project_goal.value = PHASE_GOALS.get(new_phase, '')
            
            # Update board
            self.capstone_board.set_phase(new_phase)
            
            self.app_page.update()
        except Exception as ex:
            print(f"Error changing phase: {ex}")
