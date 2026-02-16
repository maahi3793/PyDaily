import flet as ft
from services.local_session import LocalSession

def AdminDashboardView(page: ft.Page, use_sidebar=True):
    print("DEBUG: AdminDashboardView builder called")
    
    local_session = LocalSession()
    role = local_session.get("pynexus_role")
    
    # --- SECURITY GATE ---
    if role != 'admin':
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.LOCK, size=50, color=ft.Colors.RED_400),
                ft.Text("ACCESS DENIED", size=30, weight="bold", color=ft.Colors.RED_400),
                ft.Text("This area is restricted to High Command.", color=ft.Colors.GREY_400),
                ft.ElevatedButton("Return to Base", on_click=lambda _: page.go("/dashboard"), 
                                 bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
            ], alignment="center", horizontal_alignment="center", spacing=16),
            alignment=ft.Alignment(0, 0),
            expand=True,
            bgcolor="#0f172a"
        )

    # --- LAZY SERVICE ---
    _admin_service = None
    
    def get_service():
        nonlocal _admin_service
        if _admin_service is None:
            from services.admin_service import AdminService
            _admin_service = AdminService()
        return _admin_service
    
    # --- STATE ---
    selected_illustrator_day = ft.Ref[str]()
    selected_image_id = ft.Ref[str]()
    upload_status = ft.Ref[ft.Text]()
    
    selected_editor_day = ft.Ref[str]()
    selected_editor_part = ft.Ref[str]()
    editor_status = ft.Ref[ft.Text]()

    # --- HANDLERS ---
    def on_illustrator_day_change(e):
        day = int(e.control.value)
        selected_illustrator_day.current = e.control.value
        images = get_service().get_images_for_day(day)
        img_options = [ft.dropdown.Option(img['id']) for img in images]
        image_dropdown.options = img_options
        image_dropdown.value = None
        image_dropdown.disabled = False
        page.update()

    def on_image_selected(e):
        selected_image_id.current = e.control.value

    def load_pending_days(e=None):
        service = get_service()
        pending_days = [str(d) for d in service.get_days_with_pending_images()]
        illustrator_day_dropdown.options = [ft.dropdown.Option(d) for d in pending_days]
        if not pending_days:
            illustrator_day_dropdown.options = [ft.dropdown.Option("No pending images")]
        page.update()
    
    def on_regenerate(e):
        day_str = day_editor_dropdown.value
        part_str = part_editor_dropdown.value
        
        if not day_str or not part_str:
            editor_status.current.value = "⚠️ Select Day and Part."
            page.update()
            return
            
        editor_status.current.value = "🔄 Neural Engine Active..."
        editor_status.current.color = ft.Colors.BLUE_400
        page.update()
        
        day = int(day_str)
        success, msg = get_service().regenerate_content(day, part_str)
        
        if success:
            editor_status.current.value = f"✅ Regeneration Complete: {msg}"
            editor_status.current.color = ft.Colors.GREEN_400
        else:
            editor_status.current.value = f"❌ Failed: {msg}"
            editor_status.current.color = ft.Colors.RED_400
        page.update()

    # --- UI COMPONENTS ---
    image_dropdown = ft.Dropdown(label="Select Placeholder ID", expand=True, disabled=True)
    image_dropdown.on_change = on_image_selected

    day_editor_dropdown = ft.Dropdown(
        label="Select Day", expand=True,
        options=[ft.dropdown.Option(str(d)) for d in range(1, 181)]
    )
    
    part_editor_dropdown = ft.Dropdown(
        label="Select Part", expand=True,
        options=[
            ft.dropdown.Option("Part 1 (Theory)"),
            ft.dropdown.Option("Part 2 (Practice)"),
            ft.dropdown.Option("Part 3 (Mentor)"),
            ft.dropdown.Option("All Parts"),
        ]
    )

    illustrator_day_dropdown = ft.Dropdown(
        label="Select Day (click to load)", expand=True, 
        options=[ft.dropdown.Option("Loading...")],
        on_focus=load_pending_days
    )
    illustrator_day_dropdown.on_change = on_illustrator_day_change

    # --- MAIN CONTENT ---
    main_content = ft.Container(
        content=ft.Column([
            # Header
            ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.SECURITY, color="#a78bfa"),
                    ft.Text("NEXUS CONTROL ROOM", size=18, weight="bold", color="#c4b5fd"),
                ], spacing=8),
                ft.Container(expand=True),
                ft.ElevatedButton("Exit", icon=ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/dashboard"),
                                 bgcolor=ft.Colors.with_opacity(0.1, "#a78bfa"), color="#c4b5fd")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color="#334155"),
            
            ft.Text("Admin Identified: admin@pydaily.com", color=ft.Colors.GREY_500, italic=True, size=12),
            
            ft.Container(height=20),
            
            # --- THE ILLUSTRATOR ---
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.IMAGE, color=ft.Colors.BLUE_400, size=20),
                        ft.Text("THE ILLUSTRATOR", weight="bold", color=ft.Colors.BLUE_300),
                    ], spacing=8),
                    ft.Text("Inject Visuals into the Neural Stream.", size=12, color=ft.Colors.GREY_500),
                    ft.Divider(color="#334155", height=16),
                    
                    ft.Row([illustrator_day_dropdown, image_dropdown], spacing=16),
                    
                    ft.ElevatedButton(
                        "Upload & Infuse", icon=ft.Icons.UPLOAD, 
                        disabled=True,
                        tooltip="Run 'pip install --upgrade flet' to enable",
                        bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE
                    ),
                    ft.Text(ref=upload_status, size=12, italic=True)
                ], spacing=12),
                padding=20, 
                border=ft.border.all(1, ft.Colors.BLUE_700), 
                border_radius=12, 
                bgcolor="#1e293b"
            ),
            
            ft.Container(height=20),
             
            # --- THE EDITOR ---
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.EDIT, color=ft.Colors.ORANGE_400, size=20),
                        ft.Text("THE EDITOR", weight="bold", color=ft.Colors.ORANGE_300),
                    ], spacing=8),
                    ft.Text("Force Regeneration of Curriculum Content.", size=12, color=ft.Colors.GREY_500),
                    ft.Divider(color="#334155", height=16),
                    
                    ft.Row([day_editor_dropdown, part_editor_dropdown], spacing=16),
                    
                    ft.ElevatedButton("Regenerate Content", icon=ft.Icons.REFRESH, 
                                     bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, on_click=on_regenerate),
                    ft.Text(ref=editor_status, size=12, italic=True)
                ], spacing=12),
                padding=20, 
                border=ft.border.all(1, ft.Colors.ORANGE_700), 
                border_radius=12, 
                bgcolor="#1e293b"
            ),

        ], spacing=12, scroll="auto"),
        padding=40,
        expand=True,
        bgcolor="#0f172a"
    )
    
    # --- LAYOUT ---
    if use_sidebar:
        from components.sidebar import Sidebar
        return ft.Container(
            content=ft.Row([
                Sidebar(page, selected_index=3),
                main_content
            ], spacing=0, expand=True),
            expand=True
        )
    else:
        return main_content
