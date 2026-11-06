---
title: "Inheritance"
minutes: 20
prereqs: ["08-oop/03-dunder-methods"]
concepts: ["inheritance", "subclass", "super", "override", "polymorphism", "isinstance", "issubclass"]
local_only: false
hints:
  - "Employee: store name and monthly_salary in __init__; annual_pay returns self.monthly_salary * 12; describe returns f\"{self.name} earns {self.annual_pay():.2f} a year\"."
  - "Manager: class Manager(Employee): its __init__(self, name, monthly_salary, reports=None) calls super().__init__(name, monthly_salary) and then sets self.reports = list(reports) if reports else a new empty list. Override annual_pay: return super().annual_pay() + 1000 * len(self.reports)."
  - "Do not copy describe into Manager. Employee's describe calls self.annual_pay(), and Python picks the Manager version for a Manager automatically. total_payroll: sum(p.annual_pay() for p in people)."
---

## Why this matters

Often one kind of thing is a more specific version of another: a manager *is an* employee, a square *is a* shape. **Inheritance** lets a new class start from an existing one and add or change only what is different, without copying code.

## The idea

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):                       # Dog inherits from Animal
    def __init__(self, name, trick):
        super().__init__(name)           # run Animal's __init__ first
        self.trick = trick

    def speak(self):                     # override: replaces Animal's version
        return f"{self.name} barks"
```

- `super()` reaches the parent's version of a method.
- A `Dog` can use every `Animal` method it does not override.
- `isinstance(rex, Animal)` is `True` for a `Dog`; `issubclass(Dog, Animal)` is `True`.
- **Polymorphism:** code written for `Animal` works for any subclass, and each one answers `speak()` in its own way.

Use inheritance only for a true "is-a" relationship, and keep hierarchies shallow.

## Try it

Add a `Cat(Animal)` whose `speak` returns `"... meows"`. Loop over `[Dog("Rex", "sit"), Cat("Tom")]` and call `speak()` on each.

## Your turn

Write:

- `Employee(name, monthly_salary)` with `annual_pay()` (twelve months of salary) and `describe()` returning text like `Ann earns 36000.00 a year` (two decimals).
- `Manager(Employee)` with an extra `reports` list (given as an optional third argument; each manager gets their own list). A manager's `annual_pay()` is the normal pay **plus 1000 for each report**. Do not rewrite `describe`: it should work for both classes.
- `total_payroll(people)`: the sum of `annual_pay()` for a list of employees and managers.

## Recap

- `class Child(Parent):` inherits everything; override methods to change behaviour.
- `super()` calls the parent's version.
- Code that works with the parent type works with every child (polymorphism).

## Common mistakes

- **Forgetting `super().__init__(...)`**, so the parent's attributes are never set (`AttributeError`).
- **Copying the parent's code into the child** instead of calling `super()`.
- **Inheriting for convenience** when the relationship is not really "is a" (use composition, next lesson).
