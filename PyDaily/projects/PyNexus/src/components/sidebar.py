import flet as ft

class Sidebar(ft.Container):
    def __init__(self, page: ft.Page, selected_index=0):
        super().__init__()
        self.app_page = page
        
        nav_rail = ft.NavigationRail(
            selected_index=selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            bgcolor="transparent",
            group_alignment=-0.9,
            extended=True,
            expand=True,
            indicator_color=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_400),
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED, 
                    selected_icon=ft.Icons.HOME, 
                    label="Home",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED, 
                    selected_icon=ft.Icons.DASHBOARD, 
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.LIBRARY_BOOKS_OUTLINED, 
                    selected_icon=ft.Icons.LIBRARY_BOOKS, 
                    label="Library",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.VIEW_KANBAN_OUTLINED, 
                    selected_icon=ft.Icons.VIEW_KANBAN, 
                    label="Missions",
                ),
            ],
        )
        nav_rail.on_change = lambda e: self.navigate(e.control.selected_index)
        self.nav_rail = nav_rail

        # ADMIN GATE: Check Role
        from services.local_session import LocalSession
        self.session = LocalSession()
        role = self.session.get("pynexus_role")
        
        if role == 'admin':
            nav_rail.destinations.append(
                ft.NavigationRailDestination(
                    icon=ft.Icons.SECURITY_OUTLINED,
                    selected_icon=ft.Icons.SECURITY,
                    label="Control Room",
                )
            )
        
        # Logo area
        logo_area = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CODE, color=ft.Colors.BLUE_400, size=24),
                ft.Text("PyNexus", size=16, weight="bold", color=ft.Colors.BLUE_200),
            ], spacing=8),
            padding=ft.Padding(16, 20, 16, 10),
        )
        
        # Logout button with modern styling
        logout_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_300, size=18),
                ft.Text("Logout", color=ft.Colors.RED_300, size=13),
            ], spacing=8),
            padding=ft.Padding(16, 10, 16, 10),
            border_radius=8,
            ink=True,
        )
        logout_btn.on_click = lambda _: page.go("/login")
        
        # Set Container properties AFTER super().__init__()
        self.width = 200
        self.bgcolor = "#1e293b"
        self.border = ft.Border(right=ft.BorderSide(1, "#334155"))
        self.content = ft.Column([
            logo_area,
            ft.Divider(color="#334155", height=1),
            nav_rail,
            ft.Container(expand=True),
            logout_btn,
            ft.Container(height=10),
        ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=0)

    def navigate(self, index):
        routes = ["/home", "/dashboard", "/library", "/kanban", "/admin"]
        if 0 <= index < len(routes):
            self.app_page.go(routes[index])
