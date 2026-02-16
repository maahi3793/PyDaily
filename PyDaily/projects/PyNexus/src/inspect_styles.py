
import flet as ft

print("--- TextStyle ---")
try:
    print(dir(ft.TextStyle))
    print(ft.TextStyle.__init__.__doc__)
except Exception as e:
    print(e)

print("\n--- MarkdownStyleSheet ---")
try:
    print(dir(ft.MarkdownStyleSheet))
except Exception as e:
    print(e)
