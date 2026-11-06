from typing import TypedDict


# Add type hints to every function, and finish the User TypedDict.


def average(numbers):
    return sum(numbers) / len(numbers)


def find_user(users, name):
    return users.get(name)


def apply_twice(func, value):
    return func(func(value))


def greet(name="world"):
    return f"Hello, {name}!"


class User(TypedDict):
    pass


def describe(user):
    return f"{user['name']} is {user['age']}"
