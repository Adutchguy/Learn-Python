---
title: "Functions as Values, and Lambdas"
minutes: 15
prereqs: ["04-functions/04-scope-and-mutation"]
concepts: ["first-class function", "lambda", "key function", "higher-order function", "callback"]
local_only: false
hints:
  - "apply_twice(func, value): call the function you were given, twice: return func(func(value)). Note there are no quotes around func: it is a value."
  - "sort_people: sorted(people, key=lambda person: person[1], reverse=True). The lambda picks out the age from each (name, age) tuple."
  - "longest(words): max(words, key=len). When two words tie, max returns the first one it met, which is what the checks expect."
---

## Why this matters

In Python a function is a value, just like a number or a string. You can store it in a variable, put it in a list, and pass it to another function. That is how `sorted(words, key=len)` works: you handed `sorted` the function `len` and it calls it for you. This idea makes code flexible and short.

## The idea

```python
def shout(text):
    return text.upper() + "!"

say = shout            # no parentheses: this does not call it, it just gives it a second name
print(say("hi"))       # HI!

def apply_twice(func, value):
    return func(func(value))

print(apply_twice(shout, "a"))   # A!!
```

`shout` (a value) is different from `shout("a")` (a call that runs the function).

A **lambda** is a tiny function written inline when you only need it once:

```python
double = lambda n: n * 2         # same as def double(n): return n * 2
people = [("Ada", 36), ("Bo", 29)]
youngest_first = sorted(people, key=lambda person: person[1])
```

A lambda has parameters, a colon, and one expression whose value is returned automatically. If you need more than one expression, write a normal `def`.

`sorted`, `min`, `max` and `.sort` all accept a `key=` function; that is the most common use of lambdas.

## Try it

Use `max(["pear", "fig", "banana"], key=len)` and then try a lambda that picks the word with the *last letter* that comes latest in the alphabet.

## Your turn

Write three functions:

- `apply_twice(func, value)`: returns `func(func(value))`. For example `apply_twice(lambda n: n + 3, 10)` is `16`.
- `sort_people(people)`: `people` is a list of `(name, age)` tuples; return a new list sorted with the **oldest first**.
- `longest(words)`: the longest word in a list (the first one if there is a tie).

## Recap

- Functions are values: `f` is the function, `f()` calls it.
- A function can take another function as an argument (a "callback" or `key`).
- `lambda args: expression` is a one-line anonymous function.

## Common mistakes

- **Adding parentheses by accident:** `sorted(words, key=len())` calls `len` with no argument (`TypeError`). Pass `len`.
- **Cramming logic into a lambda.** If it needs more than a short expression, use `def` and give it a name.
- **Forgetting `key` takes a function, not a value:** `key=3` fails.
