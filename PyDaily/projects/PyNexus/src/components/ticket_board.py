import flet as ft

class TicketBoard(ft.Row):
    def __init__(self):
        super().__init__()
        
        # Mock Data for Prototype
        self.tickets = [
            {"title": "Fetch Bitcoin Price", "day_req": 10, "status": "LOCKED", "desc": "Use 'requests' to hit CoinGecko API."},
            {"title": "Calculate Moving Average", "day_req": 20, "status": "LOCKED", "desc": "Use 'pandas' to analyze CSV data."},
            {"title": "Build Trading Bot", "day_req": 30, "status": "LOCKED", "desc": "Automate buy/sell signals."},
        ]
        
        # Build UI in init
        todo_items = []
        locked_items = []
        
        for t in self.tickets:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(t['title'], weight="bold"),
                        ft.Text(t['desc'], size=12, italic=True),
                        ft.Text(f"Requires Day {t['day_req']}", size=10, color="red" if t['status']=="LOCKED" else "green")
                    ]),
                    padding=10
                )
            )
            if t['status'] == "LOCKED":
                locked_items.append(card)
            else:
                todo_items.append(card)

        self.controls = [
            self.build_column("LOCKED DEPTHS", locked_items, ft.Colors.GREY_900),
            self.build_column("OPEN TICKETS", todo_items, ft.Colors.BLUE_GREY_900),
            self.build_column("IN PROGRESS", [], ft.Colors.BLUE_900),
            self.build_column("SHIPPED", [], ft.Colors.GREEN_900),
        ]
        self.expand = True
        self.spacing = 16
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.START

    def build_column(self, title, items, color):
        # Determine gradient based on semantic color
        gradient_colors = {
            ft.Colors.GREY_900: ["#2d3436", "#000000"],
            ft.Colors.BLUE_GREY_900: ["#2c3e50", "#000000"],
            ft.Colors.BLUE_900: ["#0f2027", "#203a43"],
            ft.Colors.GREEN_900: ["#134e5e", "#71b280"], 
        }
        
        colors = gradient_colors.get(color, ["#111111", "#111111"])
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(title, weight="bold", size=12, color=ft.Colors.WHITE_70),
                        padding=ft.Padding(0, 0, 0, 10)
                    ),
                    ft.Column(items, spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
                ],
                spacing=0,
                expand=True,
            ),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[ft.Colors.with_opacity(0.8, c) for c in colors]
            ),
            padding=20,
            border_radius=12,
            expand=True,
            border=ft.Border.all(1, ft.Colors.WHITE_10),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#89000000",
                offset=ft.Offset(0, 4)
            )
        )

