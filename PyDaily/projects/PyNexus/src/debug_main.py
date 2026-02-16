import sys
import traceback as tb
import flet as ft
# Redirect stderr to a file to capture errors
sys.stderr = open('error_log.txt', 'w')
sys.stdout = sys.stderr

try:
    # Run the actual app
    import main
    print("Starting Flet app via debug_main...")
    ft.app(target=main.main)
except Exception as e:
    # Write full traceback to file
    print("CRASH DETECTED!")
    tb.print_exc(file=sys.stderr)
finally:
    sys.stderr.close()

print("Check error_log.txt for details")

