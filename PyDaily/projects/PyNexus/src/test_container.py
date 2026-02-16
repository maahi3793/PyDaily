import flet as ft

class Test(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True

def main(page: ft.Page):
    t = Test()
    page.add(t)
    print("success")

ft.app(target=main)
