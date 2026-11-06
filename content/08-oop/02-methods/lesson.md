---
title: "Methods: Giving Objects Behaviour"
minutes: 18
prereqs: ["08-oop/01-classes-and-objects"]
concepts: ["method", "self", "state", "instance method", "encapsulation"]
local_only: false
hints:
  - "In __init__ create self.items = {} (an empty dictionary). In add: if the name is already in self.items, add qty to the stored quantity; otherwise store the price and qty (for example as a list [price, qty])."
  - "total: sum price * qty over all items, rounded with round(..., 2). count: the sum of all the quantities. remove: del self.items[name]; a missing name raises KeyError by itself, which is what we want."
  - "most_expensive: return None when self.items is empty; otherwise max(self.items, key=lambda name: self.items[name][0]) gives the name with the highest unit price (the first one added wins a tie)."
---

## Why this matters

A **method** is a function that lives inside a class and works on one object's data. This is the heart of object-oriented programming: the data and the code that changes it travel together, so the rest of your program just asks the object to do things.

## The idea

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, by=1):      # a method: first parameter is self
        self.count += by

    def reset(self):
        self.count = 0

    def is_zero(self):
        return self.count == 0

c = Counter()
c.increment()
c.increment(5)
print(c.count)          # 6
c.reset()
```

Calling `c.increment(5)` is the same as `Counter.increment(c, 5)`: `c` becomes `self`. Inside a method, use `self.name` to read or change the object's data, and `self.other_method()` to call another method. A method with no `return` returns `None`.

## Try it

Add a method `double()` to `Counter` that doubles the count. Create two counters and check they do not affect each other.

## Your turn

Write a class `Cart` (a shopping cart) with these methods:

- `add(name, price, qty=1)`: add items. Adding a name that is already in the cart increases its quantity and keeps the original price.
- `remove(name)`: remove an item completely. A name that is not in the cart raises `KeyError`.
- `total()`: the total price, rounded to 2 decimals.
- `count()`: how many things are in the cart in all (the sum of the quantities).
- `most_expensive()`: the name of the item with the highest unit price, or `None` for an empty cart.

## Recap

- A method is a function in a class; its first parameter is `self`.
- Methods read and change the object's attributes through `self`.
- Let the object manage its own data; callers just call methods.

## Common mistakes

- **Forgetting `self.`** when using an attribute inside a method: `NameError: name 'items' is not defined`.
- **Calling a method without parentheses** (`cart.total` instead of `cart.total()`) gives a method object, not the answer.
- **Mutating a class-level dictionary or list**, which every object shares.
