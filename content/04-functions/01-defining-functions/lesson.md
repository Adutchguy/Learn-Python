---
title: "Defining and Calling Functions"
minutes: 15
prereqs: ["03-data-structures/08-comprehensions"]
concepts: ["function", "def", "parameter", "argument", "call", "indentation"]
local_only: false
hints:
  - "A function starts with def banner(text): and its body is indented. Inside, text is an ordinary variable."
  - "The border needs len(text) + 4 equals signs: \"=\" * (len(text) + 4). Print the border, the middle line, then the border again."
  - "The middle line is f\"| {text} |\". For greet, just print(f\"Hello, {name}!\"). Do not call the functions yourself: the checks do."
---

## Why this matters

You have already used functions: `print`, `len`, `input`. Now you make your own. A **function** is a named block of code you can run whenever you like. You write it once and use it many times, which means fewer bugs and shorter programs.

## The idea

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Ada")      # Hello, Ada!
greet("Bo")       # Hello, Bo!
```

- `def` starts the definition. `greet` is the function's name.
- `name` is a **parameter**: a variable that exists inside the function and receives a value each time it is called.
- The indented lines are the **body**. They run only when the function is *called*, with `greet("Ada")`. The value `"Ada"` is the **argument**.

Defining a function does not run it. Nothing prints until you call it.

A function can have several parameters, separated by commas. Arguments are matched up in order:

```python
def add_and_show(a, b):
    print(a + b)

add_and_show(2, 3)   # 5
```

## Try it

Define `shout(word)` that prints the word in capitals followed by `!`. Call it three times with different words.

## Your turn

Define two functions in the starter. The checks call them for you (do not call them yourself):

1. `greet(name)` prints `Hello, NAME!`
2. `banner(text)` prints the text in a box, with a border of `=` that is 4 longer than the text:

```text
=========
| Hello |
=========
```

## Recap

- `def name(parameters):` followed by an indented body defines a function.
- Calling `name(arguments)` runs the body with the parameters filled in.
- Defining is not calling: the code inside runs only when called.

## Common mistakes

- **Forgetting the colon** after the parentheses: `SyntaxError`.
- **Forgetting to indent the body:** `IndentationError`.
- **Defining but never calling**, so nothing happens. (Here, the checks do the calling.)
- **Wrong number of arguments:** `TypeError: greet() takes 1 positional argument but 2 were given`.
