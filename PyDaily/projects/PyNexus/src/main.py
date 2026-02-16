import flet as ft
from dotenv import load_dotenv
import logging

load_dotenv()

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== DATA CACHE SERVICE ======
class DataCache:
    """In-memory cache for lesson content and other data."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cache = {}
            cls._instance._timeline = None
        return cls._instance
    
    def get(self, key):
        return self._cache.get(key)
    
    def set(self, key, value):
        self._cache[key] = value
    
    def get_timeline(self):
        return self._timeline
    
    def set_timeline(self, data):
        self._timeline = data
    
    def clear(self):
        self._cache.clear()
        self._timeline = None

# Global cache instance
data_cache = DataCache()

def main(page: ft.Page):
    logger.info("PyNexus starting [Optimized Mode]")
    
    # ====== MODERN THEME CONFIG ======
    page.title = "PyNexus"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_icon = "assets/icon.ico"
    page.bgcolor = "#0f172a"  # Slate-900 (softer dark)
    
    page.fonts = {
        "SF Pro": "https://fonts.cdnfonts.com/s/16086/SFProDisplay-Regular.woff",
        "JetBrains Mono": "fonts/JetBrainsMono-Regular.ttf"
    }
    
    page.theme = ft.Theme(
        font_family="SF Pro",
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_400,      # Vibrant blue
            secondary="#a78bfa",             # Violet-400 (Hex to avoid Attribute Error)
            surface="#1e293b",               # Slate-800
            on_primary=ft.Colors.WHITE,
            on_secondary=ft.Colors.WHITE,
            on_surface=ft.Colors.WHITE,
        )
    )
    page.update()
    
    # ====== VIEW CACHE ======
    view_cache = {}
    current_sidebar = None
    
    # Main content container (swapped on navigation)
    main_content = ft.Container(expand=True)
    
    # Layout: Sidebar + Content
    app_layout = ft.Row([main_content], spacing=0, expand=True)
    page.add(app_layout)
    
    def navigate_to(route):
        nonlocal current_sidebar
        logger.info(f"Navigating to {route}")
        
        # Special case: Login has no sidebar
        if route == "/login":
            from views.login import LoginView
            app_layout.controls = [LoginView(page)]
            page.update()
            return
        
        # Create sidebar once
        if current_sidebar is None:
            from components.sidebar import Sidebar
            current_sidebar = Sidebar(page, selected_index=0)
        
        # Update sidebar selected index
        # Home=0, Dashboard=1, Library=2, Kanban=3, Admin=4
        route_indices = {"/home": 0, "/dashboard": 1, "/library": 2, "/kanban": 3, "/admin": 4}
        if hasattr(current_sidebar, 'nav_rail') and route in route_indices:
            current_sidebar.nav_rail.selected_index = route_indices[route]
        
        # Check cache or create view
        if route in view_cache:
            logger.info(f"Using cached view for {route}")
            view = view_cache[route]
        else:
            logger.info(f"Creating new view for {route}")
            
            if route == "/home":
                from views.home import HomeView
                # Pass authenticated user if available
                current_user = data_cache.get("user")
                view = HomeView(page, user=current_user, use_sidebar=False)
            elif route == "/dashboard":
                from views.dashboard import DashboardView
                view = DashboardView(page, use_sidebar=False)  # No embedded sidebar
            elif route == "/library":
                from views.library import LibraryView
                view = LibraryView(page, use_sidebar=False)
            elif route == "/kanban":
                from views.kanban_board import KanbanBoard
                view = KanbanBoard(page, use_sidebar=False)
            elif route == "/admin":
                from views.admin_dashboard import AdminDashboardView
                view = AdminDashboardView(page, use_sidebar=False)
            else:
                view = ft.Text(f"Unknown route: {route}")
            
            # Cache the view
            view_cache[route] = view
        
        # Update layout: Sidebar + Cached View
        app_layout.controls = [current_sidebar, view]
        page.update()
    
    # Monkey patch page.go
    page.go = navigate_to
    
    # ====== AUTO LOGIN CHECK ======
    from services.local_session import LocalSession
    from services.auth import AuthService
    
    local_session = LocalSession()
    auth_service = AuthService()
    
    try:
        token = local_session.get("pynexus_auth_token")
        if token:
            logger.info("Auto-Login: Token found, validating...")
            response = auth_service.get_user_from_token(token)
            if response and response.user:
                user = response.user
                logger.info(f"Auto-Login: Success via Token for {user.email}")
                data_cache.set("user", user)
                navigate_to("/home")
            else:
                logger.warning("Auto-Login: Token invalid or expired.")
                navigate_to("/login")
        else:
            logger.info("Auto-Login: No token. Redirecting to Login.")
            navigate_to("/login")
    except Exception as e:
        logger.error(f"Auto-Login Check Failed: {e}")
        navigate_to("/login")

if __name__ == "__main__":
    ft.app(target=main)
