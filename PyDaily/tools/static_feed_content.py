from tools import feed_templates

# Static Content for Days 1-22 (Skipping Quizzes)
# 3 Nuggets per day: Tip, Snippet, Image/Concept

STATIC_NUGGETS = {}

def add_day(day, topic, nuggets):
    STATIC_NUGGETS[day] = nuggets

# --- DAY 1: Setup ---
add_day(1, "Hello World", [
    {
        "type": "tip", "topic": "Python Setup", "title": "Did you know?",
        "content_html": feed_templates.render_gradient_card("Python Setup", "The Zen of Python", "Run `import this` in your Python console to see the hidden philosophy of Python! It includes 19 aphorisms like 'Simple is better than complex'. 🧘‍♂️"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "Python Setup", "title": "First Steps",
        "content_html": feed_templates.render_code_card("Python Setup", "Your First Script", "print('Hello, Python!')\n# Comments start with hash!", "The print function is your best friend when learning."),
        "score": 9
    },
    {
        "type": "image", "topic": "Python Setup", "title": "Concept",
        "content_html": feed_templates.render_image_card("Python Setup", "Interpreted Language", "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600&q=80", "Python is interpreted, meaning code runs line-by-line immediately. No complex compilation step needed! 🚀"),
        "media_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600&q=80", "score": 8
    }
])

# --- DAY 2: Variables ---
add_day(2, "Variables", [
    {
        "type": "tip", "topic": "Variables", "title": "Dynamic Typing",
        "content_html": feed_templates.render_gradient_card("Variables", "No Types Needed!", "In Python, you don't need to declare types like `int x`. You just say `x = 10`. Python figures it out. This is called Dynamic Typing. 🎭"),
        "score": 9
    },
    {
        "type": "snippet", "topic": "Variables", "title": "Swapping",
        "content_html": feed_templates.render_code_card("Variables", "Magic Swap", "a = 5\nb = 10\na, b = b, a\nprint(a) # 10", "You can swap variables in one line without a temporary variable! Only in Python. 🐍"),
        "score": 10
    },
    {
        "type": "image", "topic": "Variables", "title": "Concept",
        "content_html": feed_templates.render_image_card("Variables", "Variables are Labels", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&q=80", "Don't think of variables as boxes. Think of them as Stickynotes (Labels) attached to data. One data object can have many labels! 🏷️"),
        "media_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&q=80", "score": 8
    }
])

# --- DAY 4: Arithmetic ---
add_day(4, "Arithmetic", [
    {
        "type": "tip", "topic": "Arithmetic", "title": "Floor Division",
        "content_html": feed_templates.render_gradient_card("Arithmetic", "The Double Slash", "Standard division `/` always returns a float (5/2 = 2.5). Use `//` for Floor Division to get an integer (5//2 = 2). Essential for indexing! ➗"),
        "score": 9
    },
    {
        "type": "snippet", "topic": "Arithmetic", "title": "Power Operator",
        "content_html": feed_templates.render_code_card("Arithmetic", "Exponents", "print(2 ** 3)  # 8\nprint(4 ** 0.5) # 2.0 (Square Root)", "Use `**` for powers. Don't use `^` (that's a bitwise XOR operator)! ⚡"),
        "score": 8
    },
    {
        "type": "image", "topic": "Arithmetic", "title": "Concept",
        "content_html": feed_templates.render_image_card("Arithmetic", "Modulo Operator %", "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&q=80", "Modulo `%` gives you the remainder. `10 % 3 = 1`. It's perfect for checking if a number is even `n % 2 == 0` or looping arays! 🔄"),
        "media_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&q=80", "score": 10
    }
])

# --- DAY 5: Strings ---
add_day(5, "Strings", [
    {
        "type": "tip", "topic": "Strings", "title": "Immutability",
        "content_html": feed_templates.render_gradient_card("Strings", "Strings are Forever", "Strings in Python are Immutable. You cannot change a character in place. `s[0] = 'X'` will crash! You must create a new string instead. 🔒"),
        "score": 9
    },
    {
        "type": "snippet", "topic": "Strings", "title": "Repetition",
        "content_html": feed_templates.render_code_card("Strings", "String Math", "print('Na' * 8 + ' Batman!')", "You can multiply strings to repeat them! Handy for separator lines like `'-' * 80`. 🦇"),
        "score": 10
    },
    {
        "type": "image", "topic": "Strings", "title": "Concept",
        "content_html": feed_templates.render_image_card("Strings", "Quotes", "https://images.unsplash.com/photo-1455849318743-b2233052fcff?w=600&q=80", "Use single `'` or double `\"` quotes comfortably. If your string contains one type, wrap it in the other! `print(\"It's a trap!\")`. 💬"),
        "media_url": "https://images.unsplash.com/photo-1455849318743-b2233052fcff?w=600&q=80", "score": 8
    }
])

# --- DAY 7: String Methods ---
add_day(7, "String Methods", [
    {
        "type": "tip", "topic": "String Methods", "title": "Cleaning Input",
        "content_html": feed_templates.render_gradient_card("String Methods", "Strip it!", "User input often has extra spaces. Always use `.strip()` to remove leading/trailing whitespace. `'  yes '.strip()` becomes `'yes'`. 🧼"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "String Methods", "title": "Chaining",
        "content_html": feed_templates.render_code_card("String Methods", "Method Chaining", "name = '  python  '\nclean = name.strip().upper()\nprint(clean) # 'PYTHON'", "You can chain methods left-to-right. Extremely Pythonic! 🔗"),
        "score": 9
    },
    {
        "type": "image", "topic": "String Methods", "title": "Concept",
        "content_html": feed_templates.render_image_card("String Methods", "Find vs Index", "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?w=600&q=80", "Use `.find()` if you're unsure if a substring exists (returns -1). Use `.index()` if you're sure (crashes if missing). Safety first! 🔍"),
        "media_url": "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?w=600&q=80", "score": 8
    }
])

# --- DAY 8: Slicing ---
add_day(8, "String Slicing", [
    {
        "type": "tip", "topic": "Slicing", "title": "Reverse String",
        "content_html": feed_templates.render_gradient_card("Slicing", "The Magic Step", "You can reverse a string using a negative step in slicing: `text[::-1]`. It starts at the end and steps backwards! ↩️"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "Slicing", "title": "Slice Syntax",
        "content_html": feed_templates.render_code_card("Slicing", "[start:stop:step]", "s = '0123456789'\nprint(s[::2]) # '02468'\nprint(s[1:5]) # '1234'", "Remember: Stop index is Exclusive (not included). `[1:5]` gives indices 1, 2, 3, 4. 🍰"),
        "score": 9
    },
    {
        "type": "image", "topic": "Slicing", "title": "Concept",
        "content_html": feed_templates.render_image_card("Slicing", "Negative Indexing", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&q=80", "Python allows negative indices `[-1]` to access the last element. Slicing with negatives `[-3:]` means 'get the last 3 items'. Super powerful! 🔚"),
        "media_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&q=80", "score": 8
    }
])

# --- DAY 10: User Input ---
add_day(10, "User Input", [
    {
        "type": "tip", "topic": "Input", "title": "Always String",
        "content_html": feed_templates.render_gradient_card("Input", "Types Matter", "`input()` ALWAYS returns a string. Even if the user types '123'. You MUST wrap it in `int()` to do math. `int(input('Age: '))`. 🔢"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "Input", "title": "Prompt Message",
        "content_html": feed_templates.render_code_card("Input", "Clean Prompts", "name = input('Name: ')\n# vs\nprint('Name:')\nname = input()", "Pass the prompt string directly to `input()` for cleaner code. Less lines, same result! ✍️"),
        "score": 8
    },
    {
        "type": "image", "topic": "Input", "title": "Concept",
        "content_html": feed_templates.render_image_card("Input", "The Pause", "https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d?w=600&q=80", "When `input()` runs, your program HALTS and waits for the Enter key. Don't be confused if the terminal looks frozen. It's just listening! 👂"),
        "media_url": "https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d?w=600&q=80", "score": 8
    }
])

# --- DAY 11: Booleans ---
add_day(11, "Booleans", [
    {
        "type": "tip", "topic": "Booleans", "title": "Truthiness",
        "content_html": feed_templates.render_gradient_card("Booleans", "Truthy & Falsy", "Empty strings `''`, `0`, and empty lists `[]` are 'Falsy'. Everything else is 'Truthy'. You can just say `if my_list:` to check if it has items! ✅"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "Booleans", "title": "Comparison",
        "content_html": feed_templates.render_code_card("Booleans", "Chained Comparison", "age = 25\nif 18 <= age < 65:\n    print('Working Age')", "Python math logic works in code! You can chain comparisons like `x < y < z` naturally. 🔗"),
        "score": 9
    },
    {
        "type": "image", "topic": "Booleans", "title": "Concept",
        "content_html": feed_templates.render_image_card("Booleans", "True is 1", "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=600&q=80", "Did you know `True == 1` and `False == 0`? You can do math with them! `sum([True, False, True])` is 2. 🤯"),
        "media_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=600&q=80", "score": 8
    }
])

# --- DAY 13: Logical Operators ---
add_day(13, "Logic", [
    {
        "type": "tip", "topic": "Logic", "title": "Short Circuit",
        "content_html": feed_templates.render_gradient_card("Logic", "Short Circuiting", "In `A and B`, if A is False, Python doesn't even check B. It stops immediately. Useful for safety: `if user and user.is_active:` (Prevents crash if user is None). ⚡"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "Logic", "title": "Not Keyword",
        "content_html": feed_templates.render_code_card("Logic", "English Logic", "logged_in = False\nif not logged_in:\n    print('Please Login')", "Use `not` for negation. It reads like plain English. Much cleaner than `if logged_in == False`. 🗣️"),
        "score": 9
    },
    {
        "type": "image", "topic": "Logic", "title": "Concept",
        "content_html": feed_templates.render_image_card("Logic", "Order of Ops", "https://images.unsplash.com/photo-1509228627129-669043e80e81?w=600&q=80", "Priority: `not` > `and` > `or`. Use parentheses `(A or B) and C` to be explicit and avoid bugs! 🧱"),
        "media_url": "https://images.unsplash.com/photo-1509228627129-669043e80e81?w=600&q=80", "score": 8
    }
])

# --- DAY 14: Control Flow ---
add_day(14, "If Else", [
    {
        "type": "tip", "topic": "If Else", "title": "Elif",
        "content_html": feed_templates.render_gradient_card("If Else", "Why Elif?", "Use `elif` instead of multiple `if` statements. Once an `elif` matches, Python SKIPS the rest. Multiple `if`s run every single check. Efficiency! 🏎️"),
        "score": 9
    },
    {
        "type": "snippet", "topic": "If Else", "title": "Ternary Operator",
        "content_html": feed_templates.render_code_card("If Else", "One-Line If", "status = 'Adult' if age >= 18 else 'Minor'", "This is the 'Ternary Operator'. Great for assigning variables based on a condition cleanly. 1️⃣"),
        "score": 10
    },
    {
        "type": "image", "topic": "If Else", "title": "Concept",
        "content_html": feed_templates.render_image_card("If Else", "Indentation", "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&q=80", "Indentation DEFINES the block. If you mess up the spaces, your logic breaks. Stay consistent: 4 Spaces is the golden rule! 📏"),
        "media_url": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&q=80", "score": 8
    }
])

# --- DAY 16: Lists ---
add_day(16, "Lists", [
    {
        "type": "tip", "topic": "Lists", "title": "Mixed Types",
        "content_html": feed_templates.render_gradient_card("Lists", "Anything Goes", "Python lists can hold ANYTHING. `[1, 'two', 3.0, [4]]`. You can mix types, though usually it's better to keep them consistent for sanity. 🎒"),
        "score": 9
    },
    {
        "type": "snippet", "topic": "Lists", "title": "Accessing Last",
        "content_html": feed_templates.render_code_card("Lists", "Grab the End", "items = ['a', 'b', 'c']\nlast = items[-1]", "Always use `[-1]` to get the last item. Never allow `items[len(items)-1]`, that's the old C way! 🚫"),
        "score": 10
    },
    {
        "type": "image", "topic": "Lists", "title": "Concept",
        "content_html": feed_templates.render_image_card("Lists", "Mutable", "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=600&q=80", "Lists are Mutable. You can change them in-place. `lst.append(x)` modifies the original list. It doesn't return a new one! 🏗️"),
        "media_url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=600&q=80", "score": 8
    }
])

# --- DAY 17: List Methods ---
add_day(17, "List Methods", [
    {
        "type": "tip", "topic": "Methods", "title": "Append vs Extend",
        "content_html": feed_templates.render_gradient_card("Methods", "Append vs Extend", "`append([1,2])` adds the LIST as one item. `extend([1,2])` adds the NUMBERS individually. Know the difference! ➕"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "Methods", "title": "Pop",
        "content_html": feed_templates.render_code_card("Methods", "Pop it!", "tasks = ['eat', 'sleep']\ndone = tasks.pop()\nprint(done) # 'sleep'", "`.pop()` removes AND returns the last item. Perfect for Stack data structures (LIFO). 🥞"),
        "score": 9
    },
    {
        "type": "image", "topic": "Methods", "title": "Concept",
        "content_html": feed_templates.render_image_card("Methods", "Insert", "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=600&q=80", "`.insert(index, value)` lets you put things anywhere. But be careful: inserting at the start `[0]` of a huge list is slow (Python has to shift everything!). 🐢"),
        "media_url": "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=600&q=80", "score": 8
    }
])

# --- DAY 19: For Loops ---
add_day(19, "For Loops", [
    {
        "type": "tip", "topic": "For Loops", "title": "Iterate Directly",
        "content_html": feed_templates.render_gradient_card("For Loops", "No Indexes Needed", "Don't loop by index `range(len(lst))`. Loop directly: `for item in lst:`. It's cleaner, faster, and more Pythonic. 🏃"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "For Loops", "title": "Enumerate",
        "content_html": feed_templates.render_code_card("For Loops", "Need Index?", "names = ['Ali', 'Bob']\nfor i, name in enumerate(names):\n    print(f'{i}: {name}')", "If you DO need the index, use `enumerate()`. It gives you both index and value gracefully. 🔢"),
        "score": 9
    },
    {
        "type": "image", "topic": "For Loops", "title": "Concept",
        "content_html": feed_templates.render_image_card("For Loops", "Flow", "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=600&q=80", "Think of a For Loop as 'For Each' logic. It grabs item 1, processes it. Grabs item 2, processes it. Until the list is empty. 🔄"),
        "media_url": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=600&q=80", "score": 8
    }
])

# --- DAY 20: Range ---
add_day(20, "Range", [
    {
        "type": "tip", "topic": "Range", "title": "Lazy Loading",
        "content_html": feed_templates.render_gradient_card("Range", "Range is Lazy", "`range(1000000)` doesn't create a million numbers in memory. It generates them one by one as you ask for them. Extremely memory efficient! 🧠"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "Range", "title": "Steps",
        "content_html": feed_templates.render_code_card("Range", "Countdown", "for i in range(10, 0, -1):\n    print(i)\nprint('Liftoff!')", "Range takes a 3rd argument: Step. Make it negative to count down! 🚀"),
        "score": 9
    },
    {
        "type": "image", "topic": "Range", "title": "Concept",
        "content_html": feed_templates.render_image_card("Range", "The Bounds", "https://images.unsplash.com/photo-1509228627129-669043e80e81?w=600&q=80", "Start is Inclusive. Stop is Exclusive. `range(1, 5)` gives 1, 2, 3, 4. It stops BEFORE the stop number. Same as Slicing logic! 🛑"),
        "media_url": "https://images.unsplash.com/photo-1509228627129-669043e80e81?w=600&q=80", "score": 8
    }
])

# --- DAY 22: While Loops ---
add_day(22, "While Loops", [
    {
        "type": "tip", "topic": "While Loops", "title": "Infinite Danger",
        "content_html": feed_templates.render_gradient_card("While Loops", "Infinite Loops", "Always ensure your loop condition eventually becomes False! Otherwise your program runs forever until you force kill it (Ctrl+C). `while True` needs a `break`! ♾️"),
        "score": 10
    },
    {
        "type": "snippet", "topic": "While Loops", "title": "User Menu",
        "content_html": feed_templates.render_code_card("While Loops", "Game Loop", "while True:\n    cmd = input('Cmd: ')\n    if cmd == 'quit':\n        break", "This is the 'Game Loop' pattern. Run forever, check input, break when done. The heart of every game/app! 🎮"),
        "score": 9
    },
    {
        "type": "image", "topic": "While Loops", "title": "Concept",
        "content_html": feed_templates.render_image_card("While Loops", "Condition", "https://images.unsplash.com/photo-1504384308090-c54be3855833?w=600&q=80", "`while` checks logic BEFORE looping. `do-while` loops (which run at least once) don't exist in Python. Use `while True` to simulate them. 🚦"),
        "media_url": "https://images.unsplash.com/photo-1504384308090-c54be3855833?w=600&q=80", "score": 8
    }
])
