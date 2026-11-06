---
title: "Dataclasses"
minutes: 18
prereqs: ["08-oop/05-composition"]
concepts: ["dataclass", "field", "default_factory", "frozen", "order", "__post_init__", "type hints"]
local_only: false
hints:
  - "Product: put @dataclass above the class and list the fields with type hints: name: str, price: float, tags: list = field(default_factory=list). Import with from dataclasses import dataclass, field. __post_init__(self) runs after the generated __init__: raise ValueError(\"price cannot be negative\") if self.price < 0."
  - "price_with_tax(self, rate) returns round(self.price * (1 + rate), 2). Coordinate is @dataclass(frozen=True) with lat: float and lon: float. Task is @dataclass(order=True) with priority: int and title: str = field(compare=False)."
  - "frozen=True makes the object read-only and hashable, so it can be a dictionary key. order=True adds <, >, <= and >= by comparing the fields in order; compare=False leaves the title out of the comparison, so tasks sort by priority."
---

## Why this matters

Many classes are mostly a bag of fields: `__init__` copies arguments onto `self`, `__repr__` prints them, `__eq__` compares them. A **dataclass** writes all of that for you from a short list of fields.

## The idea

```python
from dataclasses import dataclass, field

@dataclass
class Player:
    name: str
    score: int = 0                       # a default value
    items: list = field(default_factory=list)   # a NEW list for each object

p = Player("Ada")
print(p)                    # Player(name='Ada', score=0, items=[])
print(p == Player("Ada"))   # True: compares all fields
```

Useful options:

- `@dataclass(frozen=True)`: instances cannot be changed after creation, and can be dictionary keys.
- `@dataclass(order=True)`: adds `<`, `>`, `<=`, `>=` using the fields in order.
- `field(compare=False)`: leave a field out of comparisons.
- `__post_init__(self)`: a method run right after the generated `__init__`, handy for validation.

The type hints are required, but Python does not enforce them.

## Try it

Make a `Player` dataclass and print one. Then add `frozen=True` and try `p.score = 5`. What error do you get?

## Your turn

Write three dataclasses:

- `Product` with fields `name`, `price` and `tags` (a list, new for each product, empty by default). A negative price raises `ValueError("price cannot be negative")`. Add a method `price_with_tax(rate)` returning the price plus tax, rounded to 2 decimals.
- `Coordinate` with `lat` and `lon`, **frozen**, so it can be used as a dictionary key.
- `Task` with `priority` (an int) and `title` (a string that is **not** used for comparing), ordered so that `sorted()` puts the lowest priority number first.

## Recap

- `@dataclass` generates `__init__`, `__repr__` and `__eq__` from the annotated fields.
- Use `field(default_factory=list)` for mutable defaults.
- `frozen=True` and `order=True` add immutability and sorting.

## Common mistakes

- **`tags: list = []`** raises `ValueError: mutable default <class 'list'> for field tags is not allowed: use default_factory`.
- **A field with a default before one without**: `TypeError: non-default argument 'x' follows default argument`.
- **Forgetting the type hint**, so the name is a plain class attribute and not a field.
