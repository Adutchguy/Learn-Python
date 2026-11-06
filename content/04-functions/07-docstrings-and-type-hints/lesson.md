---
title: "Docstrings and Type Hints"
minutes: 15
prereqs: ["04-functions/06-recursion"]
concepts: ["docstring", "type hint", "annotation", "help()", "readable code"]
local_only: false
hints:
  - "A docstring is a string on the very first line inside the function: \"\"\"Return the body mass index.\"\"\". It can be a single sentence."
  - "Annotate parameters as name: type and the result with -> type, for example def bmi(weight: float, height: float) -> float:"
  - "to_fahrenheit(celsius: float) -> float returns celsius * 9 / 5 + 32. Give it a docstring too."
---

## Why this matters

Code is read far more often than it is written, and the next reader is often you in three months. Two small habits make functions much easier to use: a **docstring** says what the function does, and **type hints** say what goes in and comes out.

## The idea

```python
def area(width: float, height: float) -> float:
    """Return the area of a rectangle."""
    return width * height
```

- The **docstring** is a triple-quoted string as the first statement. Python stores it, so `help(area)` and editors can show it. Describe *what* and *why*, not each line.
- **Type hints** annotate each parameter (`width: float`) and the return value (`-> float`). They are for people and tools: Python does **not** enforce them when the code runs.

Common types: `int`, `float`, `str`, `bool`, `list[int]`, `dict[str, int]`, and `None` for "returns nothing".

```python
def greet_all(names: list[str]) -> None:
    """Print a greeting for every name."""
    for name in names:
        print(f"Hello, {name}!")
```

A tool called a type checker (like `mypy`) can read the hints and warn you before you run the code; you will meet it in the testing module.

## Try it

Call `help(area)` after defining it. Then call `area("a", "b")` and notice Python does not complain about the hints (it will fail inside the multiplication, which is a different error).

## Your turn

The starter has a working but undocumented function `bmi`. Do two things:

1. Add a one-line docstring and type hints (`float` for both parameters and the result) to `bmi`. Do not change what it calculates.
2. Write `to_fahrenheit(celsius)` that converts Celsius to Fahrenheit (`celsius * 9 / 5 + 32`), with the same care: a docstring, and type hints `float` in and `float` out. `to_fahrenheit(100)` is `212.0`.

## Recap

- A docstring (first line in the body, triple quotes) documents a function.
- Hints like `x: int` and `-> str` describe inputs and outputs; Python ignores them at run time.
- Good names plus a short docstring beat comments on every line.

## Common mistakes

- **Putting the docstring after other code**, which makes it an ordinary string instead.
- **Believing hints are checked.** Passing the wrong type still runs.
- **A docstring that repeats the code** (`"""Multiplies a by b."""` for `a * b`). Say what it is for.
