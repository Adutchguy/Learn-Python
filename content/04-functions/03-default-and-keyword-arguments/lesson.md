---
title: "Default, Keyword and Variable Arguments"
minutes: 18
prereqs: ["04-functions/02-return-values"]
concepts: ["default argument", "keyword argument", "*args", "**kwargs", "keyword-only"]
local_only: false
hints:
  - "power: give the second parameter a default in the definition: def power(base, exponent=2): then return base ** exponent."
  - "join_words(*words, sep=\" \"): words is a tuple of everything passed. Put the parameter sep after *words and return sep.join(words)."
  - "profile(name, **details): details is a dictionary. Build the text with sorted(details.items()) and join the \"key=value\" pieces with \", \"."
---

## Why this matters

Real functions are flexible. `print("a", "b", sep="-")` takes any number of values and an optional separator. You can write functions like that too.

## The idea

**Default values** make a parameter optional:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Ada")             # 'Hello, Ada!'
greet("Ada", "Welcome")  # 'Welcome, Ada!'
```

**Keyword arguments** say which parameter you mean, so the order no longer matters and calls read well:

```python
greet(greeting="Hi", name="Bo")
```

**`*args`** collects any number of extra positional arguments into a tuple:

```python
def total(*numbers):
    return sum(numbers)

total(1, 2, 3)           # 6
```

**`**kwargs`** collects extra keyword arguments into a dictionary:

```python
def show(**info):
    return info

show(a=1, b=2)           # {'a': 1, 'b': 2}
```

A parameter placed after `*args` can only be given by keyword (`sep=` below). Parameters with defaults come after those without.

## Try it

Write `box(text, char="*")` that returns the text surrounded by `char` on each side. Call it with and without the second argument.

## Your turn

Write three functions that **return** their answers:

- `power(base, exponent=2)`: `power(3)` is `9` and `power(2, 10)` is `1024`.
- `join_words(*words, sep=" ")`: `join_words("a", "b", "c")` is `"a b c"`, and with `sep="-"` it is `"a-b-c"`.
- `profile(name, **details)`: the name, then the details sorted by key: `profile("Ada", city="London", age=36)` is `"Ada (age=36, city=London)"`. With no details it is just `"Ada"`.

## Recap

- `def f(x, y=10)` gives `y` a default; callers may leave it out.
- Keyword arguments (`f(y=1, x=2)`) name the parameter; `*args` and `**kwargs` gather extras into a tuple and a dict.
- Defaults are evaluated once: use immutable defaults like numbers, text or `None`.

## Common mistakes

- **A required parameter after a default one:** `SyntaxError: non-default argument follows default argument`.
- **A list as a default** (`def f(items=[])`): the same list is shared by every call. Use `None` and create the list inside.
- **Giving a parameter twice**, positionally and by keyword: `TypeError: got multiple values`.
