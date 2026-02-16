-- Capstone Stories Update Script for Phase 1
-- Run this in Supabase SQL Editor

-- Step 1: Delete existing Phase 1 stories
DELETE FROM capstone_stories 
WHERE project_id IN (
  SELECT id FROM capstone_projects WHERE phase = 1
);

-- Step 2: Get the project_id for Phase 1
-- Run: SELECT id FROM capstone_projects WHERE phase = 1;
-- Replace 88f8b405-e9a7-4597-b526-75bc352f269e below with your actual UUID

INSERT INTO capstone_stories (project_id, story_code, order_num, title, description, acceptance_criteria, starter_code, test_code, xp, hints)
VALUES
-- P1-S01
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S01', 1, 'Welcome Banner & Menu Display',
 'In this first story, you will set the stage for the entire application by creating a welcoming visual interface. You need to write a script that displays a distinct header and a list of available menu options to the user. This establishes the visual identity of the playground and confirms that your Python environment is set up correctly. You will focus purely on using print statements to format text output linearly. This static display is the foundation that we will animate with logic in the next step.',
 '["The program prints a welcome banner (e.g., ''--- PyNexus Playground ---'').", "The program prints a list of menu options.", "Option ''1'' is labeled as ''Calculator''.", "Option ''0'' is labeled as ''Exit''.", "The program runs from top to bottom and terminates immediately after printing."]'::jsonb,
 '# Welcome to the PyNexus Playground
# TODO: Print the welcome banner using dashes or asterisks
# ...

# TODO: Print the menu title
# ...

# TODO: Print Option 1 for ''Calculator''
# ...

# TODO: Print Option 0 for ''Exit''
# ...

# TODO: Print a footer line to make it look clean
# ...',
 'import subprocess
import sys

def test_menu_display():
    result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
    output = result.stdout.lower()
    assert "pynexus" in output, "Output should contain the app name ''PyNexus''"
    assert "1" in output and "calculator" in output, "Menu should list Calculator option"
    assert "0" in output and "exit" in output, "Menu should list Exit option"
    assert result.returncode == 0, "Script should exit cleanly"',
 10,
 '["Use the print() function to send text to the console.", "You can multiply strings (e.g., ''-'' * 20) to create separators.", "Ensure strings are enclosed in quotes.", "Python executes code sequentially from line 1 to the end."]'::jsonb
),

-- P1-S02
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S02', 2, 'Menu Loop & Exit Strategy',
 'Now that we have a visual menu, we need to make the application interactive and persistent. You will implement a ''while'' loop that keeps the program running so the user can see the menu repeatedly. You will also use the ''input'' function to capture the user''s choice and check it using an ''if'' statement. Crucially, you must implement a specific condition to break the loop when the user selects ''0'', allowing them to exit the program gracefully. This transforms your static script into a running application.',
 '["The application runs continuously in a loop.", "The menu is reprinted in every iteration of the loop.", "The program pauses to wait for user input.", "Entering ''0'' breaks the loop and prints a goodbye message.", "Entering anything else just causes the loop to repeat (for now)."]'::jsonb,
 '# TODO: Create a boolean variable to control the loop (e.g., running = True)
___ = True

# TODO: Start a while loop using that variable
while ___:
    # TODO: Paste your print statements from Story 1 here
    # ...

    # TODO: Get user input and store it in a variable ''choice''
    choice = ___

    # TODO: Check if choice is ''0'' to exit
    if choice == ___:
        print("Goodbye!")
        # TODO: Stop the loop
        ___',
 'import subprocess
import sys

def test_exit_behavior():
    result = subprocess.run([sys.executable, "main.py"], input="0\n", capture_output=True, text=True)
    assert "goodbye" in result.stdout.lower(), "Should print goodbye message on exit"
    assert result.returncode == 0

def test_loop_persistence():
    result = subprocess.run([sys.executable, "main.py"], input="invalid\n0\n", capture_output=True, text=True)
    assert result.stdout.lower().count("calculator") >= 2, "Menu should appear at least twice"',
 15,
 '["A ''while'' loop repeats code as long as its condition is True.", "Use the ''input()'' function to get text from the user.", "The ''break'' keyword immediately stops the current loop.", "Remember that input() returns a string, so compare with strings (e.g., \"0\")."]'::jsonb
),

-- P1-S03
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S03', 3, 'The Calculator Feature',
 'In this story, you will build the first real feature: a simple calculator. You will extend your menu logic to handle the choice ''1''. When selected, the program should ask for two numbers and an operation (+, -, *, /). You will use ''if'', ''elif'', and ''else'' statements to perform the correct math based on the user''s input. Since ''input'' returns strings, you must convert these inputs into integers or floats before doing arithmetic. The result should be displayed clearly before returning to the main menu.',
 '["Selecting ''1'' prompts the user for two numbers.", "The program prompts for an operation (+, -, *, /).", "Correct result is printed for valid operations.", "Division by zero is handled gracefully.", "User is returned to the main menu after the calculation."]'::jsonb,
 '    # ... inside the while loop ...
    
    # TODO: Add an elif block for choice ''1''
    elif choice == "1":
        print("--- Calculator ---")
        
        # TODO: Get first number and convert to integer
        num1 = int(___)
        
        # TODO: Get second number
        num2 = ___
        
        # TODO: Get operation symbol
        op = ___
        
        # TODO: Use if/elif to perform the math and print result
        if op == "+":
            print(num1 + num2)
        # TODO: Handle -, *, and /',
 'import subprocess
import sys

def test_addition():
    inputs = "1\n5\n3\n+\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "8" in result.stdout, "5 + 3 should result in 8"

def test_multiplication():
    inputs = "1\n4\n4\n*\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "16" in result.stdout, "4 * 4 should result in 16"',
 18,
 '["Use int() or float() to convert string input to numbers.", "Use elif to check multiple conditions.", "Ensure you are inside the main while loop.", "Strings and numbers cannot be added together without conversion."]'::jsonb
),

-- P1-S04
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S04', 4, 'String Analyzer Tool',
 'You will now add a second tool: a String Analyzer. Update the main menu to include option ''2''. When selected, the user types in any sentence or word. Your program will then output useful statistics about that text, such as the length, the uppercase version, the lowercase version, and the reversed string. This story helps you practice string methods and slicing, which are essential for handling textual data in Python.',
 '["Menu includes option ''2'' for ''String Analyzer''.", "User inputs a string to analyze.", "Program displays the length of the string.", "Program displays the string in all upper case.", "Program displays the reversed string.", "Program returns to the main menu."]'::jsonb,
 '    # ... inside the while loop ...
    
    # TODO: Add elif for choice ''2''
    elif choice == "2":
        text = input("Enter text: ")
        
        # TODO: Print length
        print("Length:", ___)
        
        # TODO: Print uppercase version
        print("Upper:", ___)
        
        # TODO: Print reversed version using slicing [::-1]
        print("Reversed:", ___)',
 'import subprocess
import sys

def test_string_analyzer():
    inputs = "2\nPython\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "6" in result.stdout, "Length of Python is 6"
    assert "PYTHON" in result.stdout, "Should print uppercase version"
    assert "nohtyP" in result.stdout, "Should print reversed version"',
 15,
 '["The len() function gives the number of characters in a string.", "Strings have built-in methods like .upper() and .lower().", "You can slice a string using [start:end:step]. A step of -1 reverses it.", "Make sure to update the main print menu to show this new option."]'::jsonb
),

-- P1-S05
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S05', 5, 'Number Guessing Game',
 'It''s time to add a game! You will implement a ''Number Guessing Game'' as option ''3''. This requires importing the ''random'' module at the top of your file. Inside this feature, you will generate a random number between 1 and 100. Then, create a nested ''while'' loop that asks the user to guess the number. The program should provide ''Too high'' or ''Too low'' feedback until the user guesses correctly. This introduces nested loops and module imports.',
 '["Menu includes option ''3'' for ''Guessing Game''.", "Program imports ''random'' module.", "A secret number is generated between 1 and 100.", "User is prompted repeatedly until they guess correctly.", "Program gives ''Too high'' or ''Too low'' feedback.", "Program prints a success message upon winning."]'::jsonb,
 'import random # TODO: Move this to the very top of the file

# ... inside the main loop ...
    elif choice == "3":
        secret = random.randint(1, 100)
        print("I am thinking of a number 1-100")
        
        # TODO: Create a boolean for the game loop
        guessing = True
        
        while guessing:
            guess = int(input("Guess: "))
            
            # TODO: Check if guess is correct, high, or low
            if guess == secret:
                print("Correct!")
                ___ = False # Stop the game loop
            elif guess < secret:
                print("Too low")
            # ... handle too high',
 'import subprocess
import sys

def test_guessing_game_flow():
    inputs = "3\n50\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "thinking of a number" in result.stdout.lower()
    assert result.returncode == 0',
 20,
 '["Import statements usually go at the very first line of the script.", "You can have a ''while'' loop inside another ''while'' loop.", "Make sure the break only stops the inner game loop, not the main menu loop.", "random.randint(a, b) includes both a and b."]'::jsonb
),

-- P1-S06
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S06', 6, 'Notes Manager (Lists)',
 'Your user might want to remember things. In this story, you will add a ''Notes'' feature (option ''4'') using a Python List. You must initialize an empty list at the start of your program (outside the main loop) to ensure data persists while the app runs. When option ''4'' is selected, show a sub-menu asking if the user wants to ''Add Note'' or ''View Notes''. This teaches you about state persistence within a session and basic list operations.',
 '["A list variable notes is initialized before the main loop.", "Menu includes option ''4'' for ''Notes''.", "Selecting ''4'' offers a sub-choice: Add (1) or View (2).", "Add: Takes user input and appends it to the list.", "View: Uses a ''for'' loop to print all stored notes.", "Notes persist between different menu selections."]'::jsonb,
 '# TODO: Initialize empty list for notes at the top level
notes = []

# ... inside main loop ...
    elif choice == "4":
        print("1. Add Note")
        print("2. View Notes")
        sub_choice = input("Select: ")
        
        if sub_choice == "1":
            note = input("Note: ")
            # TODO: Append note to the list
            ___
        elif sub_choice == "2":
            # TODO: Loop through notes and print them
            for note in ___:
                print("- " + note)',
 'import subprocess
import sys

def test_notes_persistence():
    inputs = "4\n1\nBuy Milk\n4\n2\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "Buy Milk" in result.stdout, "The note should appear when viewing"
    assert "- " in result.stdout, "Should format the list output"',
 18,
 '["Define the list variable at the very top of your file.", "Use list.append(item) to add data.", "Use ''for x in list:'' to iterate through items.", "Check indentation carefully for the sub-menu if/else blocks."]'::jsonb
),

-- P1-S07
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S07', 7, 'Settings Configuration (Dictionaries)',
 'Now you will implement a ''Settings'' menu (option ''5'') using a Python Dictionary. Dictionaries store data in key-value pairs. You will create a default configuration. When the user selects ''5'', display the current settings values by accessing the dictionary keys. Allow the user to change a specific setting, updating the value in the dictionary. This introduces key-based data storage.',
 '["A dictionary settings is initialized at the top of the file.", "Menu includes option ''5'' for ''Settings''.", "Selecting ''5'' prints the current values.", "User can toggle or change the value of ''theme''.", "The updated setting is saved and shown correctly next time.", "Program returns to main menu."]'::jsonb,
 '# TODO: Initialize settings dictionary at top
settings = {"theme": "Light", "notifications": "On"}

# ... inside main loop ...
    elif choice == "5":
        print("Current Settings:")
        # TODO: Print current theme from dictionary
        print("Theme:", ___["theme"])
        
        change = input("Change theme? (y/n): ")
        if change == "y":
            # TODO: Update the dictionary value
            settings["theme"] = "Dark"',
 'import subprocess
import sys

def test_settings_update():
    inputs = "5\ny\n5\nn\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "Dark" in result.stdout, "Theme should change to Dark after update"',
 18,
 '["Access dictionary values using square brackets: dict[\"key\"].", "Assign new values just like variables: dict[\"key\"] = new_value.", "Define the dictionary outside the loop to keep changes saved.", "Keys are case-sensitive."]'::jsonb
),

-- P1-S08
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S08', 8, 'Robust Input Validation',
 'Currently, your program crashes if a user enters letters when numbers are expected. In this story, you will harden your application by adding input validation. Before converting an input to an integer, you must check if the string contains only digits using the .isdigit() string method. If the input is invalid, print an error message and skip the operation instead of crashing. This is a critical step in making software user-friendly.',
 '["Calculator checks inputs using .isdigit() before conversion.", "Guessing Game checks inputs using .isdigit().", "If input is invalid, an error message prints.", "The program does NOT crash on bad input.", "The main menu handles invalid choices using an else block."]'::jsonb,
 '    # ... inside Calculator block ...
        num1_str = input("Enter number: ")
        
        # TODO: Check if string is digits only
        if num1_str.isdigit():
            num1 = int(num1_str)
            # ... proceed
        else:
            print("Error: Not a number!")
            # ... skip logic',
 'import subprocess
import sys

def test_bad_input_resilience():
    inputs = "1\nfive\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "Error" in result.stdout or "valid" in result.stdout, "Should warn user on bad input"
    assert result.returncode == 0, "Program should not crash"',
 12,
 '["The .isdigit() method returns True only if all characters are numbers.", "Always validate external input before processing it.", "Use else blocks to handle the invalid path.", "Do not try to convert to int() unless you are sure it will succeed."]'::jsonb
),

-- P1-S09
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S09', 9, 'Usage Statistics Tracking',
 'Let''s make the app smarter by tracking how the user interacts with it. You will create a stats dictionary at the top level to count how many times the calculator was used, how many games were played, and how many notes were written. You need to increment these counters inside the respective blocks. Finally, add a menu option ''6'' to display these statistics. This connects logic flow with data persistence.',
 '["A dictionary stats initializes counters.", "Calculator usage increments calc_uses.", "Game runs increment games_played.", "Menu option ''6'' displays all statistics.", "Counts are accurate based on session usage."]'::jsonb,
 'stats = {"calc_uses": 0, "games_played": 0}

# ... inside loop ...
    elif choice == "1":
        # TODO: Increment calc counter
        stats["calc_uses"] = stats["calc_uses"] + 1
        # ... run calculator logic

    elif choice == "6":
        # TODO: Print stats
        print("Calculator Uses:", stats["calc_uses"])',
 'import subprocess
import sys

def test_stats_tracking():
    inputs = "1\n1\n1\n+\n6\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "Calculator Uses: 1" in result.stdout, "Should track 1 use of calculator"',
 15,
 '["Increment values using dict[key] += 1.", "Ensure the stats variable is outside the loop.", "Update the counters at the beginning of the feature block."]'::jsonb
),

-- P1-S10
('88f8b405-e9a7-4597-b526-75bc352f269e', 'P1-S10', 10, 'Final Polish & Integration',
 'The logic is complete. Now, focus on the user experience (UX) and code cleanliness. Review your main.py and ensure the menu is consistent, separators are used effectively to group output, and the exit message is friendly. Ensure that if the user enters an invalid menu option, the program tells them it''s invalid instead of doing nothing. This is the final step before the playground is considered Shippable.',
 '["Menu is neatly formatted with separators.", "Invalid menu choices trigger a specific ''Invalid choice'' message.", "Code contains comments explaining the main sections.", "No dead code or unused variables remain.", "The application feels cohesive and robust."]'::jsonb,
 '    # ... inside loop ...
    
    # TODO: Add a final ''else'' to the main if/elif chain
    else:
        print("Invalid selection, please try again.")
        print("-" * 20)

    # TODO: Review all print statements for consistency
    # e.g., print("-" * 20) between sections',
 'import subprocess
import sys

def test_invalid_menu_handling():
    inputs = "99\n0\n"
    result = subprocess.run([sys.executable, "main.py"], input=inputs, capture_output=True, text=True)
    assert "invalid" in result.stdout.lower(), "Should catch invalid menu options"
    assert result.returncode == 0',
 20,
 '["An else at the end of an if/elif chain catches anything not matched previously.", "Consistent formatting makes CLI apps much easier to read.", "Comments help others understand the code.", "Test every option one last time to ensure they work together."]'::jsonb
);

-- IMPORTANT: Replace ALL '88f8b405-e9a7-4597-b526-75bc352f269e' with your actual project UUID!
-- Find it with: SELECT id FROM capstone_projects WHERE phase = 1;
