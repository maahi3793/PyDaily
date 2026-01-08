from backend.sheets_manager import SheetsManager

print("--- RESETTING SHEET TO DAY 1 ---")
sm = SheetsManager()
contacts = sm.get_all_contacts()

for person in contacts:
    print(f"Resetting {person['email']}...")
    # Update Cell C (Day) -> 1, Cell D (Status) -> pending
    # Find row first
    cell = sm.sheet.find(person['email'])
    sm.sheet.update_cell(cell.row, 3, 1) # Day
    sm.sheet.update_cell(cell.row, 4, 'pending') # Status

print("✅ All contacts reset to Day 1 / Pending.")
