---
title: "Scope: Where Variables Live"
minutes: 15
prereqs: ["04-functions/03-default-and-keyword-arguments"]
concepts: ["scope", "local variable", "global variable", "mutation", "side effect", "constant"]
local_only: false
hints:
  - "add_tax: read the module-level TAX_RATE inside the function: return round(price * (1 + TAX_RATE), 2). Do not copy the rate into a default argument."
  - "with_item must not change the list it was given. Make a new list: return cart + [item]. The + operator builds a fresh list."
  - "Another safe way to copy is list(cart) or cart[:]. Then append to the copy and return it."
---

## Why this matters

Variables created inside a function are invisible outside it. This is a feature: two functions can both use a variable called `total` without touching each other. Understanding **scope** also explains one of Python's most common surprises: functions can silently change the lists you give them.

## The idea

```python
def make_message():
    message = "hi"      # local: exists only inside this function
    return message

make_message()
print(message)          # NameError: message is not defined
```

A function can **read** a variable defined outside it:

```python
TAX_RATE = 0.2          # a "constant", written in CAPITALS by convention

def with_tax(price):
    return price * (1 + TAX_RATE)
```

But assigning to a name inside a function creates a new *local* variable; it does not change the outside one. (The `global` keyword can change that, but it makes code hard to follow. Prefer parameters and `return`.)

**Lists and dicts are different.** Calling `.append()` on a list a function received changes the caller's list too, because both names point at the same list:

```python
def add_one(items):
    items.append(1)      # changes the caller's list! (a "side effect")

mine = []
add_one(mine)
print(mine)              # [1]
```

When a function should not change its input, build a new list and return it.

## Try it

Write a function that tries to print a variable that only exists in another function. Read the `NameError`. Then call `add_one` on the same list twice and watch it grow.

## Your turn

A file starts with `TAX_RATE = 0.2`. Write two functions:

- `add_tax(price)`: the price plus tax, rounded to 2 decimal places, using `TAX_RATE`. `add_tax(10)` is `12.0`. (The checks change `TAX_RATE`, so read it inside the function.)
- `with_item(cart, item)`: a **new** list that is `cart` with `item` on the end. The original `cart` must stay unchanged.

## Recap

- Names created inside a function are local; functions can read outer names but assigning makes a new local.
- Mutating a list or dict argument changes the caller's data: avoid it unless that is the point.
- Return new values instead of changing inputs.

## Common mistakes

- **`UnboundLocalError`:** assigning to a name inside a function makes it local for the whole function, so reading it earlier fails.
- **Surprise side effects** from `.append()`, `.sort()` or `del` on an argument.
- **Overusing `global`**, which hides where values change.
