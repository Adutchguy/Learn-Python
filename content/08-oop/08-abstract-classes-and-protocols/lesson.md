---
title: "Abstract Classes and Protocols"
minutes: 20
prereqs: ["08-oop/07-properties"]
concepts: ["ABC", "abstractmethod", "abstract class", "interface", "duck typing", "Protocol", "polymorphism"]
local_only: false
hints:
  - "Shape: from abc import ABC, abstractmethod. class Shape(ABC): then mark area and perimeter with @abstractmethod above each def and give each a body of just pass (or a docstring)."
  - "Square(Shape) stores side and implements area (side * side) and perimeter (4 * side). Circle(Shape) stores radius and uses math.pi: area is math.pi * radius ** 2 and perimeter is 2 * math.pi * radius."
  - "largest: return max(shapes, key=lambda shape: shape.area()). total_area: sum(thing.area() for thing in things). Do not check the type with isinstance: anything that has an area() method should work."
---

## Why this matters

When several classes should offer the same abilities (every shape has an area), you want a clear contract: "if you are a shape, you must provide `area()`". An **abstract class** states that contract, and Python refuses to create objects that break it.

## The idea

```python
from abc import ABC, abstractmethod

class Shape(ABC):                   # an abstract base class
    @abstractmethod
    def area(self):                 # subclasses MUST implement this
        ...

    def describe(self):             # normal methods are inherited as usual
        return f"area {self.area():.1f}"

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

Shape()          # TypeError: Can't instantiate abstract class Shape ...
Square(3).describe()   # 'area 9.0'
```

A subclass that forgets an abstract method cannot be instantiated either, so the mistake shows up immediately.

Python also allows **duck typing**: a function that calls `thing.area()` works for any object with that method, related or not. When you want to describe such a contract without inheritance, `typing.Protocol` lets you write a class that lists the methods an object must have; tools like type checkers then verify it. Use an abstract class when you also want to share code or refuse bad subclasses, and plain duck typing when a method or two is enough.

## Try it

Create `class Triangle(Shape)` with only `__init__`. What error do you get when you create one? Add `area` and try again.

## Your turn

Write:

- An abstract class `Shape` with abstract methods `area()` and `perimeter()`.
- `Square(side)` and `Circle(radius)`, both subclasses of `Shape` that implement them. For a circle use `math.pi`.
- `largest(shapes)`: the shape with the biggest area.
- `total_area(things)`: the sum of the areas of anything that has an `area()` method. It must work for objects that are **not** `Shape`s, too.

## Recap

- `ABC` plus `@abstractmethod` defines a contract that subclasses must fulfil.
- Abstract classes cannot be instantiated.
- Duck typing: depend on the methods an object has, not on its class.

## Common mistakes

- **Forgetting `ABC`**: without it `@abstractmethod` is not enforced.
- **Checking `isinstance` everywhere** when calling the method would do.
- **Leaving one abstract method unimplemented**: `TypeError: Can't instantiate abstract class Square with abstract method perimeter`.
