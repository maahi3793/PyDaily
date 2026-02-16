import flet as ft
from dotenv import load_dotenv

# Temporary Debug Main
# We are bypassing the complex routing to see if Flet renders ANYTHING.

def main(page: ft.Page):
    page.title = "PyNexus Debug"
    page.theme_mode = ft.ThemeMode.DARK
    
    print("Main function started")
    page.add(ft.Text("If you can see this, Flet is working.", size=30, color="green"))
    page.update()
    print("Page updated with debug text")

if __name__ == "__main__":
    ft.app(target=main)
