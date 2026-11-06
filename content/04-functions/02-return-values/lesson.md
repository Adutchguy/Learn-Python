---
title: "Return Values"
minutes: 15
prereqs: ["04-functions/01-defining-functions"]
concepts: ["return", "print vs return", "early return", "None", "returning several values"]
local_only: false
hints:
  - "average: return sum(numbers) / len(numbers). Use return, not print, so other code can use the answer."
  - "clamp: check the two edges first with early returns: if value < low: return low, then if value > high: return high, then return value."
  - "To return two values, separate them with a comma: return min(numbers), max(numbers). Python packs them into a tuple."
---

## Why this matters

A function that only prints is a dead end: nobody can reuse its answer. A function that **returns** a value hands it back to the caller, who can store it, print it, or feed it into another function. This is how you build big programs from small pieces.

## The idea

```python
def double(n):
    return n * 2

answer = double(4)      # answer is 8
print(double(double(1)))  # 4
```

`return` ends the function immediately and sends a value back. Code after a `return` never runs.

**`print` shows a value to a person; `return` gives it to the program.**

```python
def show_double(n):
    print(n * 2)       # prints, but the function's result is None

x = show_double(4)     # prints 8, then x is None
```

A function with no `return` returns `None`.

You can return early to handle special cases first:

```python
def sign(n):
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "positive"
```

And a function can return several values at once, as a tuple:

```python
def divide(a, b):
    return a // b, a % b

quotient, remainder = divide(17, 5)   # 3 and 2
```

## Try it

Write `is_even(n)` that returns `True` or `False`. Then use it in an `if` statement: `if is_even(10):`.

## Your turn

Write three functions that **return** their answers (they must not print):

- `average(numbers)`: the average of a list of numbers, e.g. `average([2, 4, 9])` is `5.0`.
- `clamp(value, low, high)`: `value`, but not less than `low` and not more than `high`. `clamp(15, 0, 10)` is `10`.
- `min_max(numbers)`: both the smallest and the largest, as `(smallest, largest)`.

## Recap

- `return value` sends a result back and ends the function.
- Printing is not returning: without `return` the result is `None`.
- Return early for special cases, and return a comma-separated group to give back several values.

## Common mistakes

- **Printing instead of returning**, so the caller gets `None`.
- **Code after `return`**, which never runs.
- **Forgetting `return` on one branch**, so some inputs give `None`.
