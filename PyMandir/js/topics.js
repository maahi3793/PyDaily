/* ================================================
   Topics Module
   Planned Python topics CRUD
   ================================================ */

const Topics = (() => {
    const defaultTopics = [
        // Phase 1 — Getting Comfortable with Syntax and Basic Logic
        '[Phase 1] Installation, Setup, and Your First "Hello World"',
        '[Phase 1] Variables and Simple Data Types (Integers, Floats)',
        '[Phase 1] Basic Arithmetic and Order of Operations',
        '[Phase 1] Introduction to Strings (Creation and Concatenation)',
        '[Phase 1] Essential String Methods (.upper(), .lower(), .strip())',
        '[Phase 1] String Slicing and Indexing',
        '[Phase 1] User Input and Type Conversion (int(), str())',
        '[Phase 1] Booleans and Comparison Operators',
        '[Phase 1] Logical Operators (and, or, not)',
        '[Phase 1] Control Flow: The if, elif, and else statements',
        '[Phase 1] Introduction to Lists (Creating and Indexing)',
        '[Phase 1] List Methods (Append, Insert, Remove, Pop)',
        '[Phase 1] The for Loop (Iterating over Lists)',
        '[Phase 1] The range() function and Loops',
        '[Phase 1] The while Loop and Infinite Loops',
        '[Phase 1] Control Statements (break, continue, pass)',
        '[Phase 1] Introduction to Dictionaries (Key-Value pairs)',
        '[Phase 1] Dictionary Methods (.keys(), .values(), .items())',
        '[Phase 1] Introduction to Tuples (Immutability)',
        '[Phase 1] Introduction to Sets (Uniqueness)',

        // Phase 2 — Writing Reusable Code and Handling Data
        '[Phase 2] Defining Functions (def) and the return statement',
        '[Phase 2] Function Parameters vs. Arguments (Positional vs. Keyword)',
        '[Phase 2] Default Arguments and Scope (Local vs. Global)',
        '[Phase 2] Variable Length Arguments (*args)',
        '[Phase 2] Keyword Variable Arguments (**kwargs)',
        '[Phase 2] Handling Errors: try and except blocks',
        '[Phase 2] Advanced Error Handling: else, finally, and raise',
        '[Phase 2] File I/O: Reading text files',
        '[Phase 2] File I/O: Writing and Appending to files',
        '[Phase 2] Context Managers (The with statement)',
        '[Phase 2] Modules: Importing standard libraries (math, random)',
        '[Phase 2] The datetime module (Dates and Times)',
        '[Phase 2] The os module (File system navigation)',
        '[Phase 2] List Comprehensions (Basic)',
        '[Phase 2] List Comprehensions (Conditional logic)',
        '[Phase 2] Dictionary and Set Comprehensions',
        '[Phase 2] Lambda Functions (Anonymous functions)',
        '[Phase 2] High-Order Functions: map()',
        '[Phase 2] High-Order Functions: filter()',
        '[Phase 2] Sorting Data (sorted() vs .sort() and Custom Keys)',
        '[Phase 2] Virtual Environments (Why and How)',
        '[Phase 2] PIP and Package Management',
        '[Phase 2] Debugging Basics (Reading Stack Traces)',
        '[Phase 2] Introduction to f-strings (Advanced formatting)',
        '[Phase 2] Mutability vs. Immutability (Memory references)',
        '[Phase 2] The Concept of OOP (Classes vs. Instances)',

        // Phase 3 — Structuring Code Using Classes and Objects
        '[Phase 3] The Constructor: __init__ and self',
        '[Phase 3] Instance Attributes vs. Class Attributes',
        '[Phase 3] Instance Methods',
        '[Phase 3] Inheritance (Parent and Child classes)',
        '[Phase 3] The super() function',
        '[Phase 3] Polymorphism and Method Overriding',
        '[Phase 3] Encapsulation (Public, Protected, Private variables)',
        '[Phase 3] Getters and Setters (The @property decorator)',
        '[Phase 3] Class Methods (@classmethod)',
        '[Phase 3] Static Methods (@staticmethod)',
        '[Phase 3] Magic/Dunder Methods (__str__, __repr__)',
        '[Phase 3] Operator Overloading (__add__, __eq__)',
        '[Phase 3] Abstract Base Classes (ABCs)',
        '[Phase 3] Composition vs. Inheritance',

        // Phase 4 — Computer Science Fundamentals
        '[Phase 4] Introduction to Big O Notation (Time Complexity)',
        '[Phase 4] Recursion (Base cases and recursive steps)',
        '[Phase 4] Linear Search vs. Binary Search (Concept)',
        '[Phase 4] Implementing Binary Search (Iterative & Recursive)',
        '[Phase 4] Bubble Sort (And why you shouldn\'t use it)',
        '[Phase 4] Selection Sort and Insertion Sort',
        '[Phase 4] Merge Sort (Divide and Conquer logic)',
        '[Phase 4] Quick Sort (Partitioning logic)',
        '[Phase 4] Stacks (LIFO) - Implementation using Lists',
        '[Phase 4] Queues (FIFO) - Implementation using collections.deque',
        '[Phase 4] Hash Tables (How Dictionaries work under the hood)',
        '[Phase 4] Linked Lists: The Node Class',
        '[Phase 4] Linked Lists: Traversal and Appending',
        '[Phase 4] Linked Lists: Inserting and Deleting nodes',
        '[Phase 4] Trees: Introduction to Binary Trees',
        '[Phase 4] Tree Traversal: In-order, Pre-order, Post-order',
        '[Phase 4] Binary Search Trees (BST): Logic and Insertion',
        '[Phase 4] Binary Search Trees: Searching and Validation',
        '[Phase 4] Heaps and Priority Queues (heapq module)',
        '[Phase 4] Graphs: Adjacency Matrix vs. Adjacency List',
        '[Phase 4] Graph Traversal: Breadth-First Search (BFS)',
        '[Phase 4] Graph Traversal: Depth-First Search (DFS)',
        '[Phase 4] Dynamic Programming: Memoization (Top-Down)',
        '[Phase 4] Dynamic Programming: Tabulation (Bottom-Up)',
        '[Phase 4] The Two Pointer Technique',
        '[Phase 4] Sliding Window Technique',
        '[Phase 4] Backtracking (Solving the N-Queens or Sudoku)',
        '[Phase 4] Bit Manipulation Basics',
        '[Phase 4] Common Interview Problem Patterns',
        '[Phase 4] Optimization: Space vs. Time trade-offs',

        // Phase 5 — Mastering the Pythonic Way
        '[Phase 5] Iterators vs. Iterables (The Iterator Protocol)',
        '[Phase 5] Generators and the yield keyword',
        '[Phase 5] Generator Expressions (Memory efficiency)',
        '[Phase 5] Decorators: First-Class Functions concept',
        '[Phase 5] Decorators: Writing your first decorator',
        '[Phase 5] Decorators with Arguments and functools.wraps',
        '[Phase 5] Context Managers: Writing custom classes (__enter__, __exit__)',
        '[Phase 5] The contextlib module (@contextmanager)',
        '[Phase 5] Regular Expressions: Basics and Pattern Matching (re module)',
        '[Phase 5] Regular Expressions: Groups and Substitution',
        '[Phase 5] Dataclasses (Python 3.7+)',
        '[Phase 5] Enum and Constants',
        '[Phase 5] walrus operator (:=) and recent Python version features',
        '[Phase 5] Type Hinting and Static Analysis (mypy)',
        '[Phase 5] Metaclasses (The type of a class)',
        '[Phase 5] Concurrency vs. Parallelism',

        // Phase 6 — Concurrency, Architecture, and Professional Practices
        '[Phase 6] Threading in Python (I/O Bound tasks)',
        '[Phase 6] Multiprocessing (CPU Bound tasks)',
        '[Phase 6] The Global Interpreter Lock (GIL) - What and Why?',
        '[Phase 6] Asynchronous I/O: The Event Loop',
        '[Phase 6] async and await keywords (Asyncio)',
        '[Phase 6] Design Patterns: Singleton and Factory',
        '[Phase 6] Design Patterns: Observer and Strategy',
        '[Phase 6] Testing: Unit Testing with unittest',
        '[Phase 6] Testing: Introduction to pytest and Fixtures',
        '[Phase 6] Logging Best Practices (Levels, Handlers, Formatters)',
        '[Phase 6] Working with JSON and APIs (requests library)',
        '[Phase 6] Intro to Serialization (pickle and security risks)',
        '[Phase 6] Packaging your code (Setup.py / Poetry)',
        '[Phase 6] Cython and interfacing with C (Brief Overview)',
    ];

    let currentFilter = 'all';

    function init() {
        const data = Storage.load();

        // Pre-populate with default topics if empty
        if (data.topics.length === 0) {
            Storage.update(d => {
                defaultTopics.forEach((name, i) => {
                    d.topics.push({
                        id: Date.now() + i,
                        name,
                        status: 'not-started',
                        createdAt: new Date().toISOString()
                    });
                });
            });
        }

        // Add topic
        document.getElementById('btn-add-topic').addEventListener('click', addTopic);
        document.getElementById('topic-input').addEventListener('keydown', e => {
            if (e.key === 'Enter') addTopic();
        });

        // Filters
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                render();
            });
        });

        render();
    }

    function addTopic() {
        const input = document.getElementById('topic-input');
        const name = input.value.trim();
        if (!name) return;

        Storage.update(data => {
            data.topics.push({
                id: Date.now(),
                name,
                status: 'not-started',
                createdAt: new Date().toISOString()
            });
        });

        input.value = '';
        render();
    }

    function cycleStatus(id) {
        Storage.update(data => {
            const topic = data.topics.find(t => t.id === id);
            if (!topic) return;
            const order = ['not-started', 'in-progress', 'completed'];
            const idx = order.indexOf(topic.status);
            topic.status = order[(idx + 1) % order.length];
        });
        render();

        // Check achievements
        const data = Storage.load();
        const newAch = Achievements.checkAll(data);
        Storage.save(data);
        newAch.forEach((ach, i) => {
            setTimeout(() => showToast(`🏆 ${ach.icon} ${ach.name} unlocked!`), i * 1500);
        });
    }

    function deleteTopic(id) {
        Storage.update(data => {
            data.topics = data.topics.filter(t => t.id !== id);
        });
        render();
    }

    function render() {
        const data = Storage.load();
        const list = document.getElementById('topics-list');
        const emptyEl = document.getElementById('topics-empty');

        let topics = data.topics;
        if (currentFilter !== 'all') {
            topics = topics.filter(t => t.status === currentFilter);
        }

        if (topics.length === 0) {
            list.innerHTML = '';
            emptyEl.style.display = '';
            return;
        }

        emptyEl.style.display = 'none';

        const statusIcons = {
            'not-started': '',
            'in-progress': '🟡',
            'completed': '✅'
        };

        list.innerHTML = topics.map(t => `
            <div class="topic-item" data-status="${t.status}">
                <button class="topic-status-btn" data-status="${t.status}" data-id="${t.id}" title="Click to change status">
                    ${statusIcons[t.status]}
                </button>
                <span class="topic-name">${escapeHtml(t.name)}</span>
                <button class="topic-delete-btn" data-id="${t.id}" title="Delete topic">✕</button>
            </div>
        `).join('');

        // Bind events
        list.querySelectorAll('.topic-status-btn').forEach(btn => {
            btn.addEventListener('click', () => cycleStatus(parseInt(btn.dataset.id)));
        });
        list.querySelectorAll('.topic-delete-btn').forEach(btn => {
            btn.addEventListener('click', () => deleteTopic(parseInt(btn.dataset.id)));
        });
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    return { init, render };
})();
