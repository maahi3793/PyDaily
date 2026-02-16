import flet as ft
from services.auth import AuthService
from services.local_session import LocalSession

def LoginView(page: ft.Page):
    print("DEBUG: LoginView builder called")
    
    email = ft.TextField(label="Email", width=300)
    password = ft.TextField(label="Password", password=True, width=300, can_reveal_password=True)
    status_text = ft.Text(color="red")

    auth = AuthService()
    local_session = LocalSession()

    # --- ACTION: Login ---
    def on_login(e):
        status_text.value = "Authenticating..."
        status_text.color = ft.Colors.CYAN_400
        page.update()
        
        try:
            # 1. Real Login
            session = auth.login(email.value, password.value)
            
            # 2. Remember Me (Robust Local Storage)
            if remember_me.value:
                local_session.save("pynexus_email", email.value)
                local_session.save("pynexus_auth_token", session.session.access_token if hasattr(session, 'session') and session.session else "mock_token")
                print(f"DEBUG: Auth saved to local file for {email.value}")
            else:
                # Clear if unchecked
                local_session.remove("pynexus_auth_token")

            # 3. Fetch & Store Role (The Admin Gate)
            try:
                user_id = session.user.id
                role = auth.get_user_role(user_id)
                local_session.save("pynexus_role", role)
                print(f"DEBUG: Role '{role}' stored in session.")
            except Exception as role_e:
                print(f"DEBUG: Role fetch error: {role_e}")
                local_session.save("pynexus_role", "student")

            status_text.value = "Access Granted. Initializing Nexus..."
            status_text.color = ft.Colors.GREEN_400
            page.update()
            
            page.go("/dashboard")
            
        except Exception as ex:
            print(f"Login Error: {ex}")
            status_text.value = f"Access Denied: {str(ex)}"
            status_text.color = ft.Colors.RED_400
            page.update()

    remember_me = ft.Checkbox(label="Remember Me on this Node", value=False, label_style=ft.TextStyle(color="grey"))

    # --- UI: Mission Access Card ---
    card_content = ft.Column(
            [
                ft.Icon(ft.Icons.SECURITY, size=40, color=ft.Colors.CYAN_400),
                ft.Text("NEXUS COMMAND", size=12, weight="bold", color=ft.Colors.CYAN_200, font_family="JetBrains Mono"),
                ft.Text("Identify Yourself", size=24, weight="bold", font_family="SF Pro"),
                ft.Divider(height=20, color="transparent"),
                email,
                password,
                ft.Divider(height=10, color="transparent"),
                remember_me,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "INITIALIZE UPLINK", 
                    on_click=on_login, 
                    width=300,
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLACK,
                        bgcolor=ft.Colors.CYAN_400,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=5
                    )
                ),
                STATUS_TEXT := status_text # Walrus assignment for safe ref if needed
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

    login_card = ft.Container(
        content=card_content,
        padding=40,
        width=400,
        border=ft.border.all(1, ft.Colors.CYAN_900),
        border_radius=15,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.CYAN_400),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.CYAN_400),
        )
    )

    container = ft.Container(
        content=login_card,
        alignment=ft.Alignment(0, 0),
        # Background Gradient for Premium Feel
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#0b0d17", "#161b2c"],
        ),
        expand=True
    )
    
    # Auto-fill logic from LocalSession
    try:
        saved_email = local_session.get("pynexus_email")
        if saved_email:
            email.value = saved_email
            remember_me.value = True
    except Exception as e:
        print(f"Warning: Failed to read from local session: {e}")

    return container
