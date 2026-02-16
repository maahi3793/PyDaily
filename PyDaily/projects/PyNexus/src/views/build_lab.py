import flet as ft
from services.workspace import WorkspaceService

class BuildLabView(ft.Container):
    def __init__(self, day_number):
        super().__init__()
        self.day_number = day_number
        self.workspace = WorkspaceService()
        self.output_console = ft.Text(font_family="Consolas", size=12, color=ft.Colors.GREEN_ACCENT)
        self.status_ring = ft.ProgressRing(visible=False)

        self.content = ft.Column(
            [
                ft.Text("THE FORGE", size=20, weight="bold", font_family="JetBrains Mono"),
                ft.Text(f"Active Ticket: Day {self.day_number}", size=14, color="grey"),
                ft.Divider(),
                ft.Row([
                    ft.ElevatedButton(
                        "START JOB", 
                        icon=ft.Icons.CODE, 
                        on_click=self.start_job,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE, 
                            bgcolor=ft.Colors.BLUE_900,
                            shape=ft.RoundedRectangleBorder(radius=5),
                        )
                    ),
                    ft.ElevatedButton(
                        "RUN DIAGNOSTICS", 
                        icon=ft.Icons.PLAY_ARROW, 
                        on_click=self.run_tests,
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLACK, 
                            bgcolor=ft.Colors.GREEN_400,
                            shape=ft.RoundedRectangleBorder(radius=5),
                        )
                    ),
                    self.status_ring
                ]),
                ft.Container(
                    content=self.output_console,
                    bgcolor="#111111",
                    padding=10,
                    border=ft.Border.all(1, ft.Colors.GREY_800),
                    border_radius=5,
                    expand=True
                )
            ],
            expand=True
        )
        self.padding = 20
        self.bgcolor = "#222222"
        self.border_radius = 10
        self.expand = True

    def start_job(self, e):
        self.status_ring.visible = True
        self.update()
        
        msg = self.workspace.start_job(self.day_number)
        
        self.status_ring.visible = False
        self.output_console.value = f"> {msg}\n"
        self.update()

    def run_tests(self, e):
        self.status_ring.visible = True
        self.output_console.value += "> Initializing Test Protocol...\n"
        self.update()
        
        success, msg = self.workspace.run_tests(self.day_number)
        
        self.status_ring.visible = False
        if success:
            self.output_console.value += f"[SUCCESS] {msg}\n"
            self.output_console.color = ft.Colors.GREEN
        else:
            self.output_console.value += f"[FAILURE] {msg}\n"
            self.output_console.color = ft.Colors.RED
        
        self.update()
