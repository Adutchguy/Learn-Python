# Dunder Methods: Making Objects Feel Built-in

*Object-Oriented Programming · about 20 minutes*

## Why this matters

Why does `"a" + "b"` work, and `len([1, 2])`, and `3 < 5`? Because those types define special methods with **double underscores** ("dunder" methods). You can define the same methods on your own classes, so they work with `+`, `==`, `<`, `print`, `sorted` and more.

## The idea

```python
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __repr__(self):                 # how it looks in the shell and in lists
        return f"Money({self.cents})"

    def __str__(self):                  # how print() and f-strings show it
        return f"${self.cents / 100:.2f}"

    def __eq__(self, other):            # ==
        if not isinstance(other, Money):
            return NotImplemented       # "I don't know how": Python falls back
        return self.cents == other.cents

    def __lt__(self, other):            # <  (also lets sorted() work)
        return self.cents < other.cents

    def __add__(self, other):           # +
        return Money(self.cents + other.cents)
```

Other favourites: `__len__` (for `len()`), `__contains__` (for `in`), `__getitem__` (for `obj[i]`), `__bool__`. If you define only `__repr__`, `str()` uses it too. Define `__repr__` for every class; it makes debugging far easier.

## Try it

Add `__len__` to a class that holds a list, then call `len(obj)`. Print an object before and after you write `__repr__`.

## Your turn

Write two classes:

- `Vector(x, y)` with `__repr__` (`Vector(1, 2)`), `__eq__` (equal when both parts match; comparing with something that is not a `Vector` must give `False`, not crash), `__add__` (add two vectors) and `__mul__` (multiply by a number: `Vector(1, 2) * 3` is `Vector(3, 6)`).
- `Version(text)` for version numbers such as `"1.10.2"`: store the numbers as a tuple of integers. `__str__` returns the original-looking text, `__eq__` compares versions, and `__lt__` orders them so that `Version("1.10.0")` is greater than `Version("1.2.0")` and `sorted()` works on a list of versions.

## Recap

- Dunder methods let your class work with operators and built-in functions.
- `__repr__` is for programmers, `__str__` is for users.
- Return `NotImplemented` from `__eq__` and `__add__` when the other type is not supported.

## Common mistakes

- **Comparing version strings as text**: `"1.10" < "1.2"` is `True` because `"1"` is smaller than `"2"` as characters.
- **Returning a string from `__eq__` or printing instead of returning** inside `__add__`.
- **Defining `__eq__` without thinking about `__hash__`**: objects that define `__eq__` can no longer be dictionary keys or set members unless you add `__hash__`.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/08-oop/03-dunder-methods
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Vector: __repr__ returns f"Vector({self.x}, {self.y})". __add__(self, other) returns Vector(self.x + other.x, self.y + other.y). __mul__(self, k) returns Vector(self.x * k, self.y * k).

</details>

<details><summary>Hint 2</summary>

__eq__(self, other): first check isinstance(other, Vector); if it is not one, return NotImplemented (Python then answers False). Otherwise return self.x == other.x and self.y == other.y. Do the same isinstance check in __add__.

</details>

<details><summary>Hint 3</summary>

Version: in __init__ split the text on "." and store a tuple of ints. __str__ joins the numbers back with ".". __eq__ and __lt__ compare the two tuples (a tuple compares item by item, so (1, 10) is bigger than (1, 2)).

</details>
