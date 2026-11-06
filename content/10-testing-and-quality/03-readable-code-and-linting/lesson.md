---
title: "Readable Code: Style, Formatters and Linters"
minutes: 18
prereqs: ["10-testing-and-quality/01-testing-with-pytest"]
concepts: ["PEP 8", "naming conventions", "docstrings", "ruff", "black", "linting", "mutable default arguments"]
local_only: false
hints:
  - "Rename to the new names: calculate_total, is_valid_email, read_number, MAX_ITEMS. Remove the unused imports (os, sys and math), and give each function a docstring (a string right under the def line)."
  - "Replace the mutable default discounts=[] with discounts=None, then inside the function use (discounts or []). Change == None to is None, and replace the bare except: with except ValueError:."
  - "Keep every line at 79 characters or fewer, use 4 spaces for indentation and no trailing spaces. Put spaces around operators and after commas. Simplify \"if x: return True else: return False\" to return x."
---

## Why this matters

Code is read far more often than it is written, mostly by you, months later. Consistent style makes code easy to read and bugs easy to spot. Python has a shared style guide (**PEP 8**), and tools that apply it for you, so you do not have to argue about it.

## The idea

The conventions you will see in almost every Python project:

| Thing | Style | Example |
|---|---|---|
| variables, functions | `snake_case` | `total_price`, `read_number` |
| classes | `CapWords` | `ShoppingCart` |
| constants | `UPPER_CASE` | `MAX_ITEMS` |
| indentation | 4 spaces, no tabs | |
| line length | about 79 to 88 characters | |
| imports | one per line, at the top, none unused | `import os` |
| docstring | on every public function | `"""Add two numbers."""` |

A few habits prevent real bugs, not just ugliness:

- Compare with `None` using `is None`, not `== None`.
- Never use a mutable default (`def f(items=[])`): the same list is shared by every call. Use `items=None`.
- Catch specific errors (`except ValueError:`), never a bare `except:` that also hides typos and `Ctrl+C`.
- Return a condition directly: `return a > b`, not `if a > b: return True else: return False`.

Two kinds of tool help:

- A **formatter** rewrites your code layout automatically: `ruff format file.py` (or `black`).
- A **linter** reports problems without changing meaning: `ruff check file.py` finds unused imports, bad names, risky patterns. `ruff check --fix` repairs many of them.

Install with `pip install ruff` on your own computer. The checks in this lesson use a small checker that looks for the same problems, so you can practise here in the browser.

## Try it

Look at the starter code and spot as many problems as you can before reading on. Then try the table above as a checklist.

## Your turn

The starter contains messy but working code. Clean it up **without changing what it does**:

- Rename `Calc_Total` to `calculate_total`, `IsValidEmail` to `is_valid_email` and `readNumber` to `read_number`, and `maxItems` to `MAX_ITEMS`.
- Remove the unused imports.
- Fix the mutable default, the `== None` and the bare `except`.
- Add a docstring to every function.
- Keep lines to 79 characters, with no tabs and no trailing spaces.

## Recap

- Follow PEP 8: `snake_case` functions, `CapWords` classes, `UPPER_CASE` constants.
- Avoid mutable default arguments, bare `except` and `== None`.
- A formatter fixes layout; a linter finds likely mistakes. `ruff` does both.
- Clean code is easier to test and to change.

## Common mistakes

- **Renaming a function but not its callers.**
- **Fixing style and changing behaviour at the same time.** Run your tests after every cleanup.
- **Fighting the formatter.** Agree on one tool and let it decide.
