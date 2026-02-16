
import flet as ft
import sys

with open("styles_info.txt", "w") as f:
    f.write("--- TextStyle ---\n")
    try:
        f.write(str(dir(ft.TextStyle)) + "\n")
    except Exception as e:
        f.write(str(e) + "\n")

    f.write("\n--- MarkdownStyleSheet ---\n")
    try:
        f.write(str(dir(ft.MarkdownStyleSheet)) + "\n")
    except Exception as e:
        f.write(str(e) + "\n")
