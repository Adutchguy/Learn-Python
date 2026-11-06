---
title: "Catching Errors with try and except"
minutes: 15
prereqs: ["05-text-and-files/06-regular-expressions"]
concepts: ["try", "except", "exception", "ValueError", "ZeroDivisionError", "KeyError", "else", "finally"]
local_only: false
hints:
  - "to_int: put int(text) inside a try block and return it. Under except ValueError: return default. Only ValueError, not every possible error."
  - "safe_divide: try: return a / b, then except ZeroDivisionError: return None."
  - "get_age: the try block is return int(person[\"age\"]). Add except KeyError: return \"unknown\" and a second clause except (ValueError, TypeError): return \"invalid\". A tuple lets one clause catch several kinds of error."
---

## Why this matters

So far an error has meant a crash. Real programs meet bad input, missing files and surprises all the time, and a good program decides what to do about them instead of dying. Python lets you **catch** an error and carry on.

## The idea

```python
text = "abc"
try:
    number = int(text)          # Python tries this...
except ValueError:              # ...and if a ValueError happens, jumps here
    number = 0
print(number)                   # 0
```

Name the **kind** of error you expect. Catching too much hides real bugs. A few more parts:

```python
try:
    price = float(text)
except ValueError as err:       # "as err" keeps the error so you can show it
    print("Not a number:", err)
else:                           # runs only if nothing went wrong
    print("Price is", price)
finally:                        # always runs, error or not
    print("done")
```

One clause can catch several kinds: `except (ValueError, TypeError):`.

## Try it

Run the example with `text = "4.5"`, then `"abc"`, then `""`. Which of `else` and `finally` ran each time? Then try `int(None)` inside the try: that is a `TypeError`, so the `except ValueError` clause does **not** catch it.

## Your turn

Write three functions:

- `to_int(text, default=0)`: return `int(text)`, or `default` if the text is not a whole number. Anything that is not a `ValueError` should still crash (for example `to_int(None)` raises a `TypeError`).
- `safe_divide(a, b)`: return `a / b`, or `None` when `b` is zero.
- `get_age(person)`: `person` is a dictionary. Return `int(person["age"])`. If there is no `"age"` key return `"unknown"`. If the value cannot be turned into a whole number (text like `"abc"`, or `None`) return `"invalid"`.

## Recap

- `try` runs code that might fail; `except SomeError` handles that one kind of failure.
- Catch the specific errors you expect so real bugs still show up.
- `else` runs when nothing failed; `finally` always runs.

## Common mistakes

- **A bare `except:` that catches everything.** It even hides typos (`NameError`). Name the error.
- **Putting too much inside `try`.** Keep it to the lines that can actually fail.
- **Forgetting the colon or indentation** after `try:` / `except ...:`, which gives a `SyntaxError` or `IndentationError`.
