---
title: "Type Hints: Describing Your Data"
minutes: 18
prereqs: ["09-pythonic-python/05-functools"]
concepts: ["type hints", "list[int]", "X | None", "Callable", "TypedDict", "static checking"]
local_only: false
hints:
  - "average: numbers: list[float] and the return type is float. find_user: users: dict[str, int], name: str, and the result is int | None because the name may be missing."
  - "apply_twice takes func: Callable[[int], int] (a function taking one int and returning an int), value: int, and returns int. Import Callable with: from collections.abc import Callable. greet has a default: name: str = \"world\"."
  - "Write the class as: class User(TypedDict): name: str, then age: int on the next line, importing TypedDict from typing. Then describe(user: User) -> str."
---

## Why this matters

Python does not make you declare types, but you can **describe** them with type hints. Hints document your code, help your editor catch mistakes before you run anything, and are used by tools such as `mypy`, `pyright` and frameworks like FastAPI. They are never required, and Python itself ignores them when running.

## The idea

```python
def total_price(prices: list[float], tax: float = 0.0) -> float:
    return sum(prices) * (1 + tax)
```

- `name: type` describes a parameter; `-> type` describes the return value.
- Containers say what is inside: `list[int]`, `dict[str, float]`, `tuple[int, str]`, `set[str]`.
- `X | None` means "an X, or nothing". Use it for values that may be missing:

```python
def find(items: list[str], target: str) -> int | None:
    return items.index(target) if target in items else None
```

- A function parameter has the type `Callable[[argument types], return type]`:

```python
from collections.abc import Callable

def twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))
```

- A `TypedDict` describes the exact keys of a dictionary:

```python
from typing import TypedDict

class Book(TypedDict):
    title: str
    pages: int
```

The hints are stored on the function in `__annotations__`, and `typing.get_type_hints(func)` reads them. That is how the checks for this lesson look at your work. A tool like `mypy` goes further and warns you when code disagrees with the hints (try `pip install mypy` and `mypy file.py` on your own computer).

## Try it

Run the example, then call `total_price(["a"])` and see that Python still runs it (and fails only inside `sum`): hints do not enforce anything by themselves.

## Your turn

The starter has working functions without hints. Add type hints so that:

- `average(numbers)` takes a list of floats and returns a float.
- `find_user(users, name)` takes a dict of `str` to `int` and a `str`, and returns an `int` or `None`.
- `apply_twice(func, value)` takes a function from `int` to `int` and an `int`, and returns an `int`.
- `greet(name)` takes a `str` with default `"world"` and returns a `str`.
- `User` is a `TypedDict` with `name: str` and `age: int`, and `describe(user)` takes a `User` and returns a `str`.

## Recap

- Hints use `param: type` and `-> type`; they describe, they do not enforce.
- `list[int]`, `dict[str, int]`, `X | None`, `Callable[[A], B]` cover most needs.
- `TypedDict` describes a dictionary with known keys.
- Static tools such as `mypy` check the hints without running the program.

## Common mistakes

- **Believing hints are checked at runtime.** They are not.
- **Forgetting `| None`** on a function that can return nothing.
- **Using `list` with no item type** when you could say `list[int]`.
