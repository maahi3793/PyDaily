"""
Python Functions Masterclass
============================

This file is a comprehensive guide to Python functions, covering everything from
basic definitions to advanced concepts like closures and decorators.

Table of Contents:
1. Basic Function Definition
2. Parameters and Arguments
3. Return Values
4. Default Arguments
5. Keyword Arguments
6. Arbitrary Arguments (*args, **kwargs)
7. Scope and Lifetime
8. Lambda Functions
9. Documentation (Docstrings)
10. Type Hinting
11. Advanced: Decorators
"""

# ==========================================
# 1. Basic Function Definition
# ==========================================

def greet():
    """A simple function that prints a greeting."""
    # The 'def' keyword starts the function definition
    print("Hello, World!")

# Calling the function
print("--- 1. Basic Function ---")
greet()


# ==========================================
# 2. Parameters and Arguments
# ==========================================
# Parameters are the variables listed inside the parentheses in the function definition.
# Arguments are the values sent to the function when it is called.

def greet_person(name):
    """Greets a specific person."""
    print(f"Hello, {name}!")

print("\n--- 2. Parameters ---")
greet_person("Alice")  # "Alice" is the argument


# ==========================================
# 3. Return Values
# ==========================================
# Functions can return data to the caller using the 'return' keyword.
# If no return statement is used, the function returns None by default.

def add(a, b):
    return a + b

def get_user_info():
    # You can return multiple values (returns a tuple)
    name = "Bob"
    age = 30
    return name, age

print("\n--- 3. Return Values ---")
result = add(5, 3)
print(f"5 + 3 = {result}")

user_name, user_age = get_user_info()
print(f"User: {user_name}, Age: {user_age}")


# ==========================================
# 4. Default Arguments
# ==========================================
# You can provide default values for parameters.
# If the caller doesn't provide a value, the default is used.

def power(base, exponent=2):
    return base ** exponent

print("\n--- 4. Default Arguments ---")
print(f"3 to the power of 2 (default): {power(3)}")
print(f"3 to the power of 3 (provided): {power(3, 3)}")

# WARNING: Mutable Default Arguments
# Never use a mutable object (like a list) as a default argument!
# It is created once when the function is defined, not every time it's called.

def bad_append(item, list_=[]): # Don't do this!
    list_.append(item)
    return list_

def good_append(item, list_=None): # Do this instead
    if list_ is None:
        list_ = []
    list_.append(item)
    return list_


# ==========================================
# 5. Keyword Arguments
# ==========================================
# You can call functions using `key=value` syntax.
# This allows you to skip arguments (if they have defaults) or change the order.

def describe_pet(animal_type, pet_name):
    print(f"\nI have a {animal_type} named {pet_name}.")

print("\n--- 5. Keyword Arguments ---")
describe_pet(animal_type="hamster", pet_name="Harry")
describe_pet(pet_name="Harry", animal_type="hamster") # Order doesn't matter


# ==========================================
# 6. Arbitrary Arguments (*args, **kwargs)
# ==========================================
# *args: Passes a variable number of non-keyword arguments (as a tuple).
# **kwargs: Passes a variable number of keyword arguments (as a dictionary).

# Useful when you don't know how many arguments will be passed.

def make_pizza(size, *toppings):
    """Summarize the pizza we are about to make."""
    print(f"\nMaking a {size}-inch pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

print("\n--- 6. Arbitrary Arguments ---")
make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')

user_profile = build_profile('albert', 'einstein',
                             location='princeton',
                             field='physics')
print(user_profile)


# ==========================================
# 7. Scope and Lifetime
# ==========================================
# Variables defined inside a function are "local" to that function.
# Variables defined outside are "global".

x = "global"

def test_scope():
    # x = "local" # Uncommenting this would create a new local variable 'x'
    # global x # Uncommenting this allows modifying the global 'x'
    print(f"Inside function: {x}")

print("\n--- 7. Scope ---")
test_scope()
print(f"Outside function: {x}")


# ==========================================
# 8. Lambda Functions
# ==========================================
# Small anonymous functions defined with the lambda keyword.
# Syntax: lambda arguments : expression

double = lambda x: x * 2

# Often used with functions like map(), filter(), and sorted()
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
squares = list(map(lambda x: x ** 2, numbers))

print("\n--- 8. Lambda Functions ---")
print(f"Double of 5: {double(5)}")
print(f"Evens: {evens}")
print(f"Squares: {squares}")


# ==========================================
# 9. Documentation (Docstrings)
# ==========================================
# Docstrings describe what a function does.
# They are enclosed in triple quotes just below the function definition.

def area(length, width):
    """
    Calculate the area of a rectangle.

    Args:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.

    Returns:
        float: The calculated area.
    """
    return length * width

print("\n--- 9. Docstrings ---")
print(area.__doc__)


# ==========================================
# 10. Type Hinting
# ==========================================
# Python 3.5+ supports type hints to indicate the expected types of arguments and return values.
# These are not enforced by Python at runtime but are useful for developers and tools.

def greeting(name: str) -> str:
    return 'Hello ' + name

print("\n--- 10. Type Hinting ---")
print(greeting("Developer"))


# ==========================================
# 11. Advanced: Decorators
# ==========================================
# Decorators allow you to modify the behavior of a function or class.
# They are functions that take another function as an argument.

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")

print("\n--- 11. Decorators ---")
say_whee()

# This is equivalent to:
# say_whee = my_decorator(say_whee)
