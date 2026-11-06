# Properties: Controlled Attributes

*Object-Oriented Programming · about 18 minutes*

## Why this matters

Attributes are convenient, but plain ones cannot protect themselves: anyone can set `age = -5`. A **property** looks like an attribute from the outside (`obj.age`) while running code underneath, so you can validate, compute values on demand, or make something read-only, without changing how other code uses the class.

## The idea

```python
class Person:
    def __init__(self, age):
        self.age = age                   # goes through the setter below

    @property                            # the "getter": runs on  p.age
    def age(self):
        return self._age

    @age.setter                          # runs on  p.age = 30
    def age(self, value):
        if value < 0:
            raise ValueError("age cannot be negative")
        self._age = value

    @property                            # no setter: read-only
    def is_adult(self):
        return self._age >= 18
```

- The real value hides in `self._age`. A leading underscore means "internal, please do not touch".
- Assigning in `__init__` through `self.age = age` means even the first value is validated.
- A property with **no setter** is read-only: assigning raises `AttributeError`.
- Properties computed from other attributes never go out of date.

## Try it

Create a `Person`, set `p.age = -3` and read the `ValueError`. Then try `p.is_adult = True`.

## Your turn

Write two classes:

- `Temperature(celsius)` with properties:
  - `celsius`: a normal readable and writable value that raises `ValueError` mentioning `absolute zero` for anything below `-273.15` (also when creating the object).
  - `fahrenheit`: readable and writable; setting it changes the celsius value (and is validated too).
  - `kelvin`: **read-only**, celsius plus `273.15`.
- `Rectangle(width, height)` with ordinary `width` and `height` attributes and read-only computed properties `area`, `perimeter` and `is_square`.

## Recap

- `@property` makes a method behave like an attribute; `@name.setter` handles assignment.
- Use setters to validate and getters to compute.
- No setter means read-only.

## Common mistakes

- **Setting `self.celsius` inside the `celsius` setter**, which calls the setter again forever (`RecursionError`). Store in `self._celsius`.
- **Calling a property with parentheses** (`t.kelvin()`): `TypeError: 'float' object is not callable`.
- **Putting the `@property` method after the setter**, so the setter has no property to attach to.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/08-oop/07-properties
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Temperature stores the value in self._celsius. Define @property def celsius(self): return self._celsius, and a setter @celsius.setter def celsius(self, value): that raises ValueError when value < -273.15 and otherwise stores it. In __init__ write self.celsius = celsius (with no underscore) so the setter validates the first value too.

</details>

<details><summary>Hint 2</summary>

fahrenheit getter: self.celsius * 9 / 5 + 32. Its setter: self.celsius = (value - 32) * 5 / 9, which also validates. kelvin is a property with a getter only: self.celsius + 273.15. Without a setter, assigning to it raises AttributeError.

</details>

<details><summary>Hint 3</summary>

Rectangle keeps width and height as ordinary attributes. area is @property def area(self): return self.width * self.height, perimeter is 2 * (width + height), is_square compares width and height. Because they are computed on request they always match the current width and height.

</details>
