# PyDaily Curriculum Map (Refactored)

# Metadata for Phases (Goals) - Adjusted for inserted Quiz Days (~1.5x expansion)
PHASE_GOALS = {
    1: "Getting comfortable with syntax and basic logic.",
    2: "Writing reusable code and handling data.",
    3: "Structuring code using Classes and Objects.",
    4: "Computer Science fundamentals necessary for interviews and optimization.",
    5: "Mastering the 'Pythonic' way and internal mechanics.",
    6: "Concurrency, Architecture, and Professional Practices."
}

def get_phase_info(day):
    # Phase 1: Originally 20 topics -> ~30 days
    if 1 <= day <= 30: return 1, PHASE_GOALS[1]
    
    # Phase 2: Originally 25 topics -> ~38 days (Ends ~Day 68)
    if 31 <= day <= 68: return 2, PHASE_GOALS[2]
    
    # Phase 3: Originally 15 topics -> ~23 days (Ends ~Day 90)
    if 69 <= day <= 90: return 3, PHASE_GOALS[3]
    
    # Phase 4: Originally 30 topics -> ~45 days (Ends ~Day 135)
    if 91 <= day <= 135: return 4, PHASE_GOALS[4]
    
    # Phase 5: Originally 15 topics -> ~23 days (Ends ~Day 158)
    if 136 <= day <= 158: return 5, PHASE_GOALS[5]
    
    # Phase 6: Originally 15 topics -> ~23 days (Ends ~Day 181)
    if 159 <= day <= 185: return 6, PHASE_GOALS[6]
    
    return 1, PHASE_GOALS[1] # Default

def get_deep_dive_attrs(day, topic):
    """
    Returns (url, source_name) for a smart deep dive link.
    Returns None if no link should be shown (e.g. Quiz Day).
    """
    if "Quiz" in topic or "Review" in topic:
        return None
    
    # URL encoded helper
    topic_query = topic.replace(" ", "+")
    
    # Day 1-40: Novice (Programiz)
    if day <= 40:
        return (
            f"https://www.google.com/search?q=site:programiz.com+python+{topic_query}&btnI=1",
            "Programiz"
        )
    
    # Day 41-100: Intermediate (Real Python)
    elif day <= 100:
        return (
            f"https://www.google.com/search?q=site:realpython.com+{topic_query}&btnI=1",
            "Real Python"
        )
        
    # Day 101-179: Advanced (Docs)
    elif day <= 179:
        return (
            f"https://www.google.com/search?q=site:docs.python.org/3+{topic_query}&btnI=1",
            "Official Docs"
        )
        
    # Day 180+: Infinite (GeeksforGeeks / StackOverflow)
    else:
        return (
            f"https://www.google.com/search?q=site:geeksforgeeks.org+python+{topic_query}&btnI=1",
            "GeeksforGeeks"
        )

# Topic Map (Auto-Generated with Quiz Intervals)
TOPICS = {
    1: "Installation, Setup, and Your First 'Hello World'",
    2: "Variables and Simple Data Types (Integers, Floats)",
    3: "Quiz Day (Review)",
    4: "Basic Arithmetic and Order of Operations",
    5: "Introduction to Strings (Creation and Concatenation)",
    6: "Quiz Day (Review)",
    7: "Essential String Methods (.upper(), .lower(), .strip())",
    8: "String Slicing and Indexing",
    9: "Quiz Day (Review)",
    10: "User Input and Type Conversion (int(), str())",
    11: "Booleans and Comparison Operators",
    12: "Quiz Day (Review)",
    13: "Logical Operators (and, or, not)",
    14: "Control Flow: The if, elif, and else statements",
    15: "Quiz Day (Review)",
    16: "Introduction to Lists (Creating and Indexing)",
    17: "List Methods (Append, Insert, Remove, Pop)",
    18: "Quiz Day (Review)",
    19: "The for Loop (Iterating over Lists)",
    20: "The range() function and Loops",
    21: "Quiz Day (Review)",
    22: "The while Loop and Infinite Loops",
    23: "Control Statements (break, continue, pass)",
    24: "Quiz Day (Review)",
    25: "Introduction to Dictionaries (Key-Value pairs)",
    26: "Dictionary Methods (.keys(), .values(), .items())",
    27: "Quiz Day (Review)",
    28: "Introduction to Tuples (Immutability)",
    29: "Introduction to Sets (Uniqueness)",
    30: "Quiz Day (Review)",
    31: "Defining Functions (def) and the return statement",
    32: "Function Parameters vs. Arguments (Positional vs. Keyword)",
    33: "Quiz Day (Review)",
    34: "Default Arguments and Scope (Local vs. Global)",
    35: "Variable Length Arguments (*args)",
    36: "Quiz Day (Review)",
    37: "Keyword Variable Arguments (**kwargs)",
    38: "Handling Errors: try and except blocks",
    39: "Quiz Day (Review)",
    40: "Advanced Error Handling: else, finally, and raise",
    41: "File I/O: Reading text files",
    42: "Quiz Day (Review)",
    43: "File I/O: Writing and Appending to files",
    44: "Context Managers (The with statement)",
    45: "Quiz Day (Review)",
    46: "Modules: Importing standard libraries (math, random)",
    47: "The datetime module (Dates and Times)",
    48: "Quiz Day (Review)",
    49: "The os module (File system navigation)",
    50: "List Comprehensions (Basic)",
    51: "Quiz Day (Review)",
    52: "List Comprehensions (Conditional logic)",
    53: "Dictionary and Set Comprehensions",
    54: "Quiz Day (Review)",
    55: "Lambda Functions (Anonymous functions)",
    56: "High-Order Functions: map()",
    57: "Quiz Day (Review)",
    58: "High-Order Functions: filter()",
    59: "Sorting Data (sorted() vs .sort() and Custom Keys)",
    60: "Quiz Day (Review)",
    61: "Virtual Environments (Why and How)",
    62: "PIP and Package Management",
    63: "Quiz Day (Review)",
    64: "Debugging Basics (Reading Stack Traces)",
    65: "Introduction to f-strings (Advanced formatting)",
    66: "Quiz Day (Review)",
    67: "Mutability vs. Immutability (Memory references)",
    68: "The Concept of OOP (Classes vs. Instances)",
    69: "Quiz Day (Review)",
    70: "The Constructor: __init__ and self",
    71: "Instance Attributes vs. Class Attributes",
    72: "Quiz Day (Review)",
    73: "Instance Methods",
    74: "Inheritance (Parent and Child classes)",
    75: "Quiz Day (Review)",
    76: "The super() function",
    77: "Polymorphism and Method Overriding",
    78: "Quiz Day (Review)",
    79: "Encapsulation (Public, Protected, Private variables)",
    80: "Getters and Setters (The @property decorator)",
    81: "Quiz Day (Review)",
    82: "Class Methods (@classmethod)",
    83: "Static Methods (@staticmethod)",
    84: "Quiz Day (Review)",
    85: "Magic/Dunder Methods (__str__, __repr__)",
    86: "Operator Overloading (__add__, __eq__)",
    87: "Quiz Day (Review)",
    88: "Abstract Base Classes (ABCs)",
    89: "Composition vs. Inheritance",
    90: "Quiz Day (Review)",
    91: "Introduction to Big O Notation (Time Complexity)",
    92: "Recursion (Base cases and recursive steps)",
    93: "Quiz Day (Review)",
    94: "Linear Search vs. Binary Search (Concept)",
    95: "Implementing Binary Search (Iterative & Recursive)",
    96: "Quiz Day (Review)",
    97: "Bubble Sort (And why you shouldn't use it)",
    98: "Selection Sort and Insertion Sort",
    99: "Quiz Day (Review)",
    100: "Merge Sort (Divide and Conquer logic)",
    101: "Quick Sort (Partitioning logic)",
    102: "Quiz Day (Review)",
    103: "Stacks (LIFO) - Implementation using Lists",
    104: "Queues (FIFO) - Implementation using collections.deque",
    105: "Quiz Day (Review)",
    106: "Hash Tables (How Dictionaries work under the hood)",
    107: "Linked Lists: The Node Class",
    108: "Quiz Day (Review)",
    109: "Linked Lists: Traversal and Appending",
    110: "Linked Lists: Inserting and Deleting nodes",
    111: "Quiz Day (Review)",
    112: "Trees: Introduction to Binary Trees",
    113: "Tree Traversal: In-order, Pre-order, Post-order",
    114: "Quiz Day (Review)",
    115: "Binary Search Trees (BST): Logic and Insertion",
    116: "Binary Search Trees: Searching and Validation",
    117: "Quiz Day (Review)",
    118: "Heaps and Priority Queues (heapq module)",
    119: "Graphs: Adjacency Matrix vs. Adjacency List",
    120: "Quiz Day (Review)",
    121: "Graph Traversal: Breadth-First Search (BFS)",
    122: "Graph Traversal: Depth-First Search (DFS)",
    123: "Quiz Day (Review)",
    124: "Dynamic Programming: Memoization (Top-Down)",
    125: "Dynamic Programming: Tabulation (Bottom-Up)",
    126: "Quiz Day (Review)",
    127: "The Two Pointer Technique",
    128: "Sliding Window Technique",
    129: "Quiz Day (Review)",
    130: "Backtracking (Solving the N-Queens or Sudoku)",
    131: "Bit Manipulation Basics",
    132: "Quiz Day (Review)",
    133: "Common Interview Problem Patterns",
    134: "Optimization: Space vs. Time trade-offs",
    135: "Quiz Day (Review)",
    136: "Iterators vs. Iterables (The Iterator Protocol)",
    137: "Generators and the yield keyword",
    138: "Quiz Day (Review)",
    139: "Generator Expressions (Memory efficiency)",
    140: "Decorators: First-Class Functions concept",
    141: "Quiz Day (Review)",
    142: "Decorators: Writing your first decorator",
    143: "Decorators with Arguments and functools.wraps",
    144: "Quiz Day (Review)",
    145: "Context Managers: Writing custom classes (__enter__, __exit__)",
    146: "The contextlib module (@contextmanager)",
    147: "Quiz Day (Review)",
    148: "Regular Expressions: Basics and Pattern Matching (re module)",
    149: "Regular Expressions: Groups and Substitution",
    150: "Quiz Day (Review)",
    151: "Dataclasses (Python 3.7+)",
    152: "Enum and Constants",
    153: "Quiz Day (Review)",
    154: "walrus operator (:=) and recent Python version features",
    155: "Type Hinting and Static Analysis (mypy)",
    156: "Quiz Day (Review)",
    157: "Metaclasses (The type of a class)",
    158: "Concurrency vs. Parallelism",
    159: "Quiz Day (Review)",
    160: "Threading in Python (I/O Bound tasks)",
    161: "Multiprocessing (CPU Bound tasks)",
    162: "Quiz Day (Review)",
    163: "The Global Interpreter Lock (GIL) - What and Why?",
    164: "Asynchronous I/O: The Event Loop",
    165: "Quiz Day (Review)",
    166: "async and await keywords (Asyncio)",
    167: "Design Patterns: Singleton and Factory",
    168: "Quiz Day (Review)",
    169: "Design Patterns: Observer and Strategy",
    170: "Testing: Unit Testing with unittest",
    171: "Quiz Day (Review)",
    172: "Testing: Introduction to pytest and Fixtures",
    173: "Logging Best Practices (Levels, Handlers, Formatters)",
    174: "Quiz Day (Review)",
    175: "Working with JSON and APIs (requests library)",
    176: "Intro to Serialization (pickle and security risks)",
    177: "Quiz Day (Review)",
    178: "Packaging your code (Setup.py / Poetry)",
    179: "Cython and interfacing with C (Brief Overview)",
}
