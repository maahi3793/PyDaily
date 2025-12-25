# PyDaily Curriculum Map

# Metadata for Phases (Goals)
PHASE_GOALS = {
    1: "Getting comfortable with syntax and basic logic.",
    2: "Writing reusable code and handling data.",
    3: "Structuring code using Classes and Objects.",
    4: "Computer Science fundamentals necessary for interviews and optimization.",
    5: "Mastering the 'Pythonic' way and internal mechanics.",
    6: "Concurrency, Architecture, and Professional Practices."
}

def get_phase_info(day):
    if 1 <= day <= 20: return 1, PHASE_GOALS[1]
    if 21 <= day <= 45: return 2, PHASE_GOALS[2]
    if 46 <= day <= 60: return 3, PHASE_GOALS[3]
    if 61 <= day <= 90: return 4, PHASE_GOALS[4]
    if 91 <= day <= 105: return 5, PHASE_GOALS[5]
    if 106 <= day <= 120: return 6, PHASE_GOALS[6]
    return 1, PHASE_GOALS[1] # Default

# Topic Map
TOPICS = {
    # Phase 1: The Absolute Fundamentals
    1: "Installation, Setup, and Your First 'Hello World'",
    2: "Variables and Simple Data Types (Integers, Floats)",
    3: "Basic Arithmetic and Order of Operations",
    4: "Introduction to Strings (Creation and Concatenation)",
    5: "Essential String Methods (.upper(), .lower(), .strip())",
    6: "String Slicing and Indexing",
    7: "User Input and Type Conversion (int(), str())",
    8: "Booleans and Comparison Operators",
    9: "Logical Operators (and, or, not)",
    10: "Control Flow: The if, elif, and else statements",
    11: "Introduction to Lists (Creating and Indexing)",
    12: "List Methods (Append, Insert, Remove, Pop)",
    13: "The for Loop (Iterating over Lists)",
    14: "The range() function and Loops",
    15: "The while Loop and Infinite Loops",
    16: "Control Statements (break, continue, pass)",
    17: "Introduction to Dictionaries (Key-Value pairs)",
    18: "Dictionary Methods (.keys(), .values(), .items())",
    19: "Introduction to Tuples (Immutability)",
    20: "Introduction to Sets (Uniqueness)",

    # Phase 2: Modular Programming & Intermediate Concepts
    21: "Defining Functions (def) and the return statement",
    22: "Function Parameters vs. Arguments (Positional vs. Keyword)",
    23: "Default Arguments and Scope (Local vs. Global)",
    24: "Variable Length Arguments (*args)",
    25: "Keyword Variable Arguments (**kwargs)",
    26: "Handling Errors: try and except blocks",
    27: "Advanced Error Handling: else, finally, and raise",
    28: "File I/O: Reading text files",
    29: "File I/O: Writing and Appending to files",
    30: "Context Managers (The with statement)",
    31: "Modules: Importing standard libraries (math, random)",
    32: "The datetime module (Dates and Times)",
    33: "The os module (File system navigation)",
    34: "List Comprehensions (Basic)",
    35: "List Comprehensions (Conditional logic)",
    36: "Dictionary and Set Comprehensions",
    37: "Lambda Functions (Anonymous functions)",
    38: "High-Order Functions: map()",
    39: "High-Order Functions: filter()",
    40: "Sorting Data (sorted() vs .sort() and Custom Keys)",
    41: "Virtual Environments (Why and How)",
    42: "PIP and Package Management",
    43: "Debugging Basics (Reading Stack Traces)",
    44: "Introduction to f-strings (Advanced formatting)",
    45: "Mutability vs. Immutability (Memory references)",

    # Phase 3: Object-Oriented Programming (OOP)
    46: "The Concept of OOP (Classes vs. Instances)",
    47: "The Constructor: __init__ and self",
    48: "Instance Attributes vs. Class Attributes",
    49: "Instance Methods",
    50: "Inheritance (Parent and Child classes)",
    51: "The super() function",
    52: "Polymorphism and Method Overriding",
    53: "Encapsulation (Public, Protected, Private variables)",
    54: "Getters and Setters (The @property decorator)",
    55: "Class Methods (@classmethod)",
    56: "Static Methods (@staticmethod)",
    57: "Magic/Dunder Methods (__str__, __repr__)",
    58: "Operator Overloading (__add__, __eq__)",
    59: "Abstract Base Classes (ABCs)",
    60: "Composition vs. Inheritance",

    # Phase 4: Data Structures & Algorithms
    61: "Introduction to Big O Notation (Time Complexity)",
    62: "Recursion (Base cases and recursive steps)",
    63: "Linear Search vs. Binary Search (Concept)",
    64: "Implementing Binary Search (Iterative & Recursive)",
    65: "Bubble Sort (And why you shouldn't use it)",
    66: "Selection Sort and Insertion Sort",
    67: "Merge Sort (Divide and Conquer logic)",
    68: "Quick Sort (Partitioning logic)",
    69: "Stacks (LIFO) - Implementation using Lists",
    70: "Queues (FIFO) - Implementation using collections.deque",
    71: "Hash Tables (How Dictionaries work under the hood)",
    72: "Linked Lists: The Node Class",
    73: "Linked Lists: Traversal and Appending",
    74: "Linked Lists: Inserting and Deleting nodes",
    75: "Trees: Introduction to Binary Trees",
    76: "Tree Traversal: In-order, Pre-order, Post-order",
    77: "Binary Search Trees (BST): Logic and Insertion",
    78: "Binary Search Trees: Searching and Validation",
    79: "Heaps and Priority Queues (heapq module)",
    80: "Graphs: Adjacency Matrix vs. Adjacency List",
    81: "Graph Traversal: Breadth-First Search (BFS)",
    82: "Graph Traversal: Depth-First Search (DFS)",
    83: "Dynamic Programming: Memoization (Top-Down)",
    84: "Dynamic Programming: Tabulation (Bottom-Up)",
    85: "The Two Pointer Technique",
    86: "Sliding Window Technique",
    87: "Backtracking (Solving the N-Queens or Sudoku)",
    88: "Bit Manipulation Basics",
    89: "Common Interview Problem Patterns",
    90: "Optimization: Space vs. Time trade-offs",

    # Phase 5: Advanced Python Features
    91: "Iterators vs. Iterables (The Iterator Protocol)",
    92: "Generators and the yield keyword",
    93: "Generator Expressions (Memory efficiency)",
    94: "Decorators: First-Class Functions concept",
    95: "Decorators: Writing your first decorator",
    96: "Decorators with Arguments and functools.wraps",
    97: "Context Managers: Writing custom classes (__enter__, __exit__)",
    98: "The contextlib module (@contextmanager)",
    99: "Regular Expressions: Basics and Pattern Matching (re module)",
    100: "Regular Expressions: Groups and Substitution",
    101: "Dataclasses (Python 3.7+)",
    102: "Enum and Constants",
    103: "walrus operator (:=) and recent Python version features",
    104: "Type Hinting and Static Analysis (mypy)",
    105: "Metaclasses (The type of a class)",

    # Phase 6: Expert Topics & System Design
    106: "Concurrency vs. Parallelism",
    107: "Threading in Python (I/O Bound tasks)",
    108: "Multiprocessing (CPU Bound tasks)",
    109: "The Global Interpreter Lock (GIL) - What and Why?",
    110: "Asynchronous I/O: The Event Loop",
    111: "async and await keywords (Asyncio)",
    112: "Design Patterns: Singleton and Factory",
    113: "Design Patterns: Observer and Strategy",
    114: "Testing: Unit Testing with unittest",
    115: "Testing: Introduction to pytest and Fixtures",
    116: "Logging Best Practices (Levels, Handlers, Formatters)",
    117: "Working with JSON and APIs (requests library)",
    118: "Intro to Serialization (pickle and security risks)",
    119: "Packaging your code (Setup.py / Poetry)",
    120: "Cython and interfacing with C (Brief Overview)"
}
