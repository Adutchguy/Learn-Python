---
title: "Raising Your Own Exceptions"
minutes: 18
prereqs: ["06-errors-and-debugging/01-try-and-except"]
concepts: ["raise", "ValueError", "TypeError", "custom exception", "error message", "validation"]
local_only: false
hints:
  - "validate_age: first check the type with isinstance(age, int) and raise TypeError(\"age must be a whole number\"). Then check the range and raise ValueError(\"age must be between 0 and 150\"). Return age at the end."
  - "OutOfStock is a one-line class: class OutOfStock(Exception): pass. In take, look up have = stock.get(item, 0); if have < quantity: raise OutOfStock(f\"only {have} {item} left, wanted {quantity}\"). Otherwise subtract and return the new count."
  - "parse_percent: if not text.endswith(\"%\"), raise ValueError(f\"not a percentage: {text!r}\"). Convert text[:-1] with int() inside try/except ValueError and raise the same ValueError message from the except block. Finally check 0 <= value <= 100."
---

## Why this matters

Catching errors is half the story. The other half is **raising** them yourself: when a function is given something it cannot work with, stopping loudly with a clear message is better than quietly returning nonsense.

## The idea

```python
def set_volume(level):
    if not 0 <= level <= 10:
        raise ValueError(f"volume must be 0-10, got {level}")
    return level
```

Pick the built-in error that fits: `ValueError` (right type, bad value), `TypeError` (wrong type), `KeyError`, `IndexError`... A good message says what was wrong **and what was received**.

You can also define an error for your own program. Treat these two lines as a recipe for now (Module 8 explains classes):

```python
class OutOfStock(Exception):
    pass
```

Then `raise OutOfStock("no apples left")` works, and callers can write `except OutOfStock:`. A bare `raise` inside an `except` block re-raises the error you just caught.

## Try it

Call `set_volume(11)` without a `try` and read the traceback. Then wrap the call in `try`/`except ValueError as err` and print `err`.

## Your turn

Write:

- `validate_age(age)`: raise `TypeError("age must be a whole number")` if `age` is not an `int`; raise `ValueError("age must be between 0 and 150")` if it is outside 0 to 150; otherwise return `age`.
- A custom error `OutOfStock` (a subclass of `Exception`).
- `take(stock, item, quantity=1)`: `stock` is a dictionary of item to count. If there are fewer than `quantity`, raise `OutOfStock` with the message `only 2 apple left, wanted 5` (the real numbers and name). Otherwise subtract `quantity` and return the new count.
- `parse_percent(text)`: turn `"45%"` into `45`. A text without a trailing `%` or with a non-whole number before it raises `ValueError("not a percentage: 'abc'")` (showing the text with `!r`). A value outside 0 to 100 raises `ValueError` whose message starts with `percentage out of range`.

## Recap

- `raise SomeError("message")` stops the function and hands the error to the caller.
- Choose the closest built-in error, and say what was received in the message.
- `class MyError(Exception): pass` creates an error type of your own.

## Common mistakes

- **Returning an error code instead of raising**, which callers forget to check.
- **Vague messages** like `"invalid"`. Include the bad value.
- **Raising a class that is not an exception**, which gives a `TypeError: exceptions must derive from BaseException`.
