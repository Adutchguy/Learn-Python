# Classes and Objects

*Object-Oriented Programming · about 18 minutes*

## Why this matters

So far your data and your functions have lived apart. A **class** bundles them: it describes a kind of thing, with its own data and its own abilities. Each thing made from it is an **object** (an *instance*). You have used objects all along: every list, string and dictionary is one.

## The idea

```python
class Dog:
    def __init__(self, name, age=1):   # runs when you create a Dog
        self.name = name               # attributes: data stored on this object
        self.age = age

rex = Dog("Rex", 3)                    # create an instance
fido = Dog("Fido")
print(rex.name, rex.age)               # Rex 3
print(fido.age)                        # 1
rex.age = 4                            # change only Rex
```

- `__init__` is the **constructor**; it sets up a new object.
- `self` is the object being created or used. Python passes it in for you, but you must list it first.
- Class names use `CamelCase`; attributes use `snake_case`.

## Try it

Create two `Dog` objects, change one's `age`, and print both. Then print `type(rex)` and `isinstance(rex, Dog)`.

## Your turn

Write:

- `class Point` with attributes `x` and `y`, both defaulting to `0`. `Point()` is the origin and `Point(3, 4)` has `x == 3`.
- `class Book(title, author, pages)` with those three attributes, plus `pages_read` starting at `0` and `notes` starting as a new empty list (every book needs **its own** list).
- `make_library(rows)`: `rows` is a list of `(title, author, pages)` tuples. Return a list of `Book` objects, one per row, in order.

## Recap

- A class describes a kind of object; `ClassName(...)` creates an instance.
- `__init__(self, ...)` sets up attributes with `self.name = value`.
- Each object keeps its own attribute values.

## Common mistakes

- **Forgetting `self`** in the method definition: `TypeError: __init__() takes 1 positional argument but 2 were given`.
- **Writing `x = x` instead of `self.x = x`**, so nothing is stored (`AttributeError` later).
- **A mutable default** such as `def __init__(self, notes=[])`, which is shared by every object.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/08-oop/01-classes-and-objects
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

A class starts with class Point: and an __init__ method: def __init__(self, x=0, y=0): then self.x = x and self.y = y. Every method's first parameter is self.

</details>

<details><summary>Hint 2</summary>

Book is the same pattern with title, author and pages. Create the notes list INSIDE __init__ (self.notes = []) and set self.pages_read = 0 there too, so every book has its own list.

</details>

<details><summary>Hint 3</summary>

make_library: build one Book per row. A list comprehension works: [Book(title, author, pages) for title, author, pages in rows].

</details>
