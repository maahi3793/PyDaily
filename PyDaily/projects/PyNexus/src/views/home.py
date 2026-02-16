"""
Home View - The Nexus HUD.
Gamified Landing Page with Agent Stats, Mission Log, and Profile Management.
"""
import flet as ft
import random
from services.auth import AuthService
from services.progress_tracker import ProgressTracker
from services.local_session import LocalSession

TIPS = [
    "Snake Bite: Use snake_case for variables and functions in Python!",
    "Snake Bite: List comprehensions are a concise way to create lists.",
    "Snake Bite: The 'zip()' function combines two iterables effortlessly.",
    "Snake Bite: 'enumerate()' gives you both index and value in loops.",
    "Snake Bite: Use 'if __name__ == \"__main__\":' to control script execution.",
    "Snake Bite: Python's 'set' is great for removing duplicates.",
    "Snake Bite: f-strings (f'Box {x}') are faster and cleaner than .format().",
    "Snake Bite: Context managers ('with open...') ensure files close safely."
]

RANKS = [
    (0, "Initiate"),
    (1000, "PyPadawan"),
    (5000, "PyKnight"),
    (10000, "PyMaster"),
    (25000, "Grandmaster"),
    (100000, "Architect")
]

class HomeView(ft.Container):
    def __init__(self, page: ft.Page, user=None, use_sidebar=True):
        super().__init__(expand=True, padding=0) # Container Init
        self.app_page = page
        self.user = user
        self.use_sidebar = use_sidebar
        print("DEBUG: HomeView Initializing (Full Rewrite)...")
        
        # Services
        self.auth = AuthService()
        self.progress = ProgressTracker()
        self.session = LocalSession()
        
        # Data Setup
        if not self.user:
            self.user = self.auth.get_user()

        if self.user:
            print(f"DEBUG: HomeView received user: {self.user.email}")
        else:
            print("DEBUG: HomeView - No User found!")

        self.user_name = self._fetch_user_name()
        self.user_avatar = self.session.get("pynexus_user_avatar")
        self.tip = random.choice(TIPS)
        
        # Build Components
        self.hud = self.build_hud()
        self.action_area = self.build_action_area()
        self.info_area = self.build_info_area()
        self.profile_dialog = self.build_profile_dialog()

        # Main Layout
        main_content = ft.Container(
            content=ft.Column([
                self.hud,
                ft.Container(height=30),
                self.action_area,
                ft.Container(height=30),
                self.info_area,
            ], expand=True, spacing=0, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            expand=True,
            # Iron Man Theme Background
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=["#0f172a", "#020617"]
            )
        )

        # Content Setup
        if self.use_sidebar:
            from components.sidebar import Sidebar
            self.content = ft.Row([
                Sidebar(self.app_page, selected_index=0),
                main_content
            ], spacing=0, expand=True)
        else:
            self.content = main_content

    # Lifecycle Hooks
    def did_mount(self):
        pass

    def will_unmount(self):
        pass

    # --- Profile Dialog Methods ---
    def open_profile_dialog(self, e):
        print("DEBUG: Opening Profile Dialog (Overlay Method)...")
        try:
            if self.profile_dialog not in self.app_page.overlay:
                self.app_page.overlay.append(self.profile_dialog)
            self.profile_dialog.open = True
            self.app_page.update()
            print("DEBUG: Profile Dialog Opened via Overlay")
        except Exception as ex:
            print(f"DEBUG: Overlay method failed: {ex}")

    def close_profile_dialog(self, e):
        self.profile_dialog.open = False
        self.app_page.update()

    def _fetch_user_name(self):
        # 1. Local Override
        local_name = self.session.get("pynexus_user_name")
        if local_name: 
            return local_name
        
        # 2. DB Profile
        if self.user:
            try:
                profile_data = self.auth.get_user_profile(self.user.id)
                db_name = profile_data.get('full_name') or profile_data.get('name') or profile_data.get('username')
                if db_name:
                    if " (Student)" in db_name:
                        db_name = db_name.replace(" (Student)", "").strip()
                    self.session.save("pynexus_user_name", db_name)
                    return db_name
            except Exception as e:
                print(f"DEBUG: Failed to fetch profile name: {e}")

            # 3. Auth Metadata
            if self.user.user_metadata:
                meta_name = self.user.user_metadata.get('full_name') or self.user.user_metadata.get('name')
                if meta_name: 
                    if " (Student)" in meta_name:
                        meta_name = meta_name.replace(" (Student)", "").strip()
                    return meta_name
            
        # 4. Email Fallback
        if self.user and self.user.email:
            return self.user.email.split('@')[0].upper()
            
        return "Agent"
    
    def get_rank_title(self, xp):
        title = "Initiate"
        for threshold, name in RANKS:
            if xp >= threshold:
                title = name
        return title

    # --- UI Builders ---
    def build_hud(self):
        """Builds the Gamified Header (Nexus HUD)."""
        total_xp = self.progress.get_total_xp()
        level = self.progress.get_level()
        streak = self.progress.get_streak()
        rank_title = self.get_rank_title(total_xp)
        
        # Avatar Logic
        avatar_content = ft.Icon(ft.Icons.PERSON, color=ft.Colors.CYAN_200, size=40)
        if self.user_avatar:
             avatar_content = ft.Image(src=self.user_avatar, width=80, height=80, border_radius=50, fit="cover")

        return ft.Container(
            content=ft.Row([
                # Left: Identity & Level
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=avatar_content,
                            padding=15 if not self.user_avatar else 0, # Remove padding if image
                            width=80, height=80,
                            border=ft.Border.all(2, ft.Colors.CYAN_400),
                            border_radius=50,
                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.3, ft.Colors.CYAN_400)),
                            on_click=self.open_profile_dialog,
                            tooltip="Edit Profile"
                        ),
                        ft.Column([
                            ft.Text(f"WELCOME, {self.user_name}", size=14, color=ft.Colors.CYAN_100, weight="bold"),
                            ft.Row([
                                ft.Text(f"LEVEL {level}", size=32, weight="bold", color=ft.Colors.WHITE, font_family="Consolas"),
                                ft.Container(
                                    content=ft.Text(rank_title.upper(), size=12, color=ft.Colors.BLACK, weight="bold"),
                                    bgcolor=ft.Colors.CYAN_400,
                                    padding=ft.Padding(8, 4, 8, 4),
                                    border_radius=4,
                                    tooltip="Earn XP to rank up!"
                                )
                            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                        ], spacing=4),
                    ], spacing=25),
                ),
                
                # Right: Stats Matrix
                ft.Row([
                    # Streak
                    ft.Column([
                        ft.Text("STREAK", size=12, color=ft.Colors.GREY_500, weight="bold"),
                        ft.Row([
                            ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.ORANGE_400, size=24),
                            ft.Text(f"{streak} DAYS", size=24, color=ft.Colors.ORANGE_300, weight="bold"),
                        ], spacing=6),
                    ], spacing=6, alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.VerticalDivider(width=40, color=ft.Colors.WHITE_10),
                    
                    # XP Display (Simplified)
                    ft.Column([
                        ft.Text("TOTAL XP", size=12, color=ft.Colors.CYAN_200, weight="bold"),
                        ft.Text(f"{total_xp:,} XP", size=24, color=ft.Colors.CYAN_400, font_family="Consolas", weight="bold"),
                        ft.Text(f"Next: {self.progress.get_next_level_progress()[1]} in level", size=10, color=ft.Colors.GREY_500),
                    ], spacing=6),
                ], spacing=0),
                
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=35,
            bgcolor=ft.Colors.with_opacity(0.4, "#1e293b"),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.CYAN_400)),
            border_radius=20,
        )

    def build_action_area(self):
        """Builds the 'Resume Training' button."""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PLAY_ARROW, color=ft.Colors.BLACK, size=40),
                        ft.Column([
                            ft.Text("RESUME TRAINING", size=20, weight="bold", color=ft.Colors.BLACK),
                            ft.Text("Continue your Python Missions", size=14, color="#0f172a"),
                        ], spacing=2)
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.Colors.CYAN_400,
                    padding=ft.Padding(60, 25, 60, 25),
                    border_radius=16,
                    on_click=lambda _: self.app_page.go("/kanban"),
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=30, color=ft.Colors.with_opacity(0.5, ft.Colors.CYAN_400)),
                    ink=True,
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.Padding(0, 10, 0, 10)
        )
    
    def build_info_area(self):
        """Mission Log and Tips."""
        # Fake mission log if empty (for demo)
        recent_missions = self.progress.data.get("completed", {})
        mission_items = []
        
        # Sort by date desc
        sorted_missions = sorted(
            recent_missions.items(), 
            key=lambda x: x[1].get("completed_at", ""), 
            reverse=True
        )[:5]

        if not sorted_missions:
            mission_items.append(ft.Text("No missions completed yet. Start training!", color=ft.Colors.GREY_500, size=12))
        else:
            for m_id, data in sorted_missions:
                mission_items.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400, size=16),
                            ft.Text(f"Mission {m_id}", color=ft.Colors.WHITE, size=12),
                            ft.Container(expand=True),
                            ft.Text(f"+{data.get('xp',0)} XP", color=ft.Colors.CYAN_200, size=12, font_family="Consolas"),
                        ]),
                        padding=5,
                        border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.WHITE_10))
                    )
                )

        return ft.Row([
            # Left: Mission Log
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.HISTORY, color=ft.Colors.PURPLE_300, size=20),
                        ft.Text("MISSION LOG", weight="bold", color=ft.Colors.PURPLE_200),
                    ]),
                    ft.Divider(color=ft.Colors.WHITE_10),
                    ft.Column(mission_items, spacing=2),
                ]),
                expand=True,
                bgcolor=ft.Colors.with_opacity(0.2, "#1e293b"),
                border=ft.Border.all(1, ft.Colors.WHITE_10),
                border_radius=12,
                padding=20,
                height=200,
            ),
            
            # Right: Snake Bites (Tips)
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=ft.Colors.YELLOW_300, size=20),
                        ft.Text("SNAKE BITES", weight="bold", color=ft.Colors.YELLOW_200),
                    ]),
                    ft.Divider(color=ft.Colors.WHITE_10),
                    ft.Container(
                        content=ft.Text(self.tip, size=16, color=ft.Colors.WHITE, italic=True, text_align=ft.TextAlign.CENTER),
                        alignment=ft.Alignment(0, 0),
                        expand=True
                    )
                ]),
                expand=True,
                bgcolor=ft.Colors.with_opacity(0.2, "#1e293b"),
                border=ft.Border.all(1, ft.Colors.WHITE_10),
                border_radius=12,
                padding=20,
                height=200,
            ),
        ], spacing=20)

    def build_profile_dialog(self):
        self.name_input = ft.TextField(label="Agent Name", value=self.user_name, color="white", border_color=ft.Colors.CYAN_400)
        
        # Cyberpunk Archetypes
        self.archetypes = [
            {"name": "The Hacker", "src": "https://api.dicebear.com/9.x/bottts-neutral/png?seed=Hacker", "color": ft.Colors.GREEN_400},
            {"name": "The Coder", "src": "https://api.dicebear.com/9.x/avataaars/png?seed=Coder&backgroundColor=b6e3f4", "color": ft.Colors.BLUE_400},
            {"name": "The AI", "src": "https://api.dicebear.com/9.x/bottts-neutral/png?seed=AI", "color": ft.Colors.PURPLE_400},
            {"name": "The Glitch", "src": "https://api.dicebear.com/9.x/bottts-neutral/png?seed=Glitch", "color": ft.Colors.RED_400},
            {"name": "The Punk", "src": "https://api.dicebear.com/9.x/avataaars/png?seed=Punk&clothing=hoodie&eyes=squint", "color": ft.Colors.ORANGE_400},
            {"name": "The Ghost", "src": "https://api.dicebear.com/9.x/bottts-neutral/png?seed=Ghost", "color": ft.Colors.CYAN_400},
        ]
        
        self.selected_avatar_src = self.user_avatar if self.user_avatar else self.archetypes[0]["src"]
        self.avatar_controls = []

        # Build Grid
        grid_items = []
        for arch in self.archetypes:
            is_selected = (arch["src"] == self.selected_avatar_src)
            img = ft.Container(
                content=ft.Image(src=arch["src"], width=60, height=60, border_radius=30),
                border=ft.Border.all(3, arch["color"] if is_selected else ft.Colors.TRANSPARENT),
                border_radius=35,
                padding=2,
                tooltip=arch["name"],
                on_click=lambda e, src=arch["src"]: self.select_avatar(src),
                data=arch["src"] # Store src in data for safe usage if needed
            )
            grid_items.append(img)
            self.avatar_controls.append(img)

        # Helper to update selection visually
        self.avatar_grid = ft.Row(controls=grid_items, wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=10)

        # Optional generic URL input
        self.avatar_url_input = ft.TextField(
            label="Or Custom URL", 
            value=self.user_avatar if self.user_avatar else "",
            hint_text="https://...",
            color="white", 
            border_color=ft.Colors.GREY_700,
            text_size=12,
            height=40,
            on_change=lambda e: self.select_avatar(e.control.value)
        )
        
        upload_content = [
            self.name_input,
            ft.Container(height=10),
            ft.Text("SELECT ARCHETYPE", size=10, color=ft.Colors.CYAN_200, weight="bold"),
            self.avatar_grid,
            ft.Container(height=10),
            self.avatar_url_input,
        ]
        
        return ft.AlertDialog(
            title=ft.Text("Edit Profile"),
            content=ft.Column(upload_content, height=300, tight=True, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_profile_dialog),
                ft.TextButton("Save", on_click=self.save_profile),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#1e293b",
        )

    def select_avatar(self, src):
        """Updates the selected avatar state."""
        self.selected_avatar_src = src
        self.avatar_url_input.value = src
        # Update Visuals
        for ctr in self.avatar_controls:
            # Check if this control's image src matches selected
            if ctr.data == src:
                ctr.border = ft.Border.all(3, ft.Colors.CYAN_400) # Highlight
            else:
                ctr.border = ft.Border.all(3, ft.Colors.TRANSPARENT)
            ctr.update()
        self.avatar_url_input.update()

    def save_profile(self, e):
        # Name
        new_name = self.name_input.value
        if new_name:
            self.session.save("pynexus_user_name", new_name)
        
        # Avatar URL (from selection)
        if self.selected_avatar_src:
             self.session.save("pynexus_user_avatar", self.selected_avatar_src)
        
        self.profile_dialog.open = False
        # Update State
        self.user_name = self._fetch_user_name()
        self.user_avatar = self.session.get("pynexus_user_avatar")
        
        # Rebuild HUD
        self.hud.content = self.build_hud().content 
        self.app_page.update()
