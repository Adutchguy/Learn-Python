from collections.abc import Callable
from typing import TypedDict


def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)


def find_user(users: dict[str, int], name: str) -> int | None:
    return users.get(name)


def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))


def greet(name: str = "world") -> str:
    return f"Hello, {name}!"


class User(TypedDict):
    name: str
    age: int


def describe(user: User) -> str:
    return f"{user['name']} is {user['age']}"
