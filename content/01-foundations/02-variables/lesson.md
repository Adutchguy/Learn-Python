---
title: Variables
minutes: 12
prereqs: ["01-foundations/01-hello-world"]
concepts: [variable, assignment, number, arithmetic]
local_only: false
hints:
  - "A variable is created with the = sign: the name goes on the left and the value (or a calculation) goes on the right."
  - "You want a variable called total. Its value is the price multiplied by the quantity. In Python, multiplication is the * symbol."
  - "Write: total = price * quantity   and then, on the next line: print(total)"
---

## Why this matters

Programs work with information: prices, names, scores. A **variable** is a name you give to a piece of information so you can use it again later.

## The idea

You create a variable with `=`. The name goes on the left, the value on the right:

```python
age = 30
name = "Sam"
```

This is called **assignment**. Read it as "let `age` be 30", not as the equals sign from maths class.

Once a variable exists you can use its name anywhere you could use the value:

```python
age = 30
print(age)        # shows 30
print(age + 1)    # shows 31
```

You can do arithmetic with `+` (add), `-` (subtract), `*` (multiply) and `/` (divide). A variable can also hold the *result* of a calculation:

```python
apples = 3
pears = 4
fruit = apples + pears
print(fruit)      # shows 7
```

Lines starting with `#` are **comments**: Python ignores them, so you can leave notes for humans.

## Try it

Use the editor to create a few variables of your own and print them. Try changing a value and running the program again. Everything that uses that variable changes with it.

## Your turn

A coffee shop sells coffee for `3.75` dollars a cup, and you are buying `4` cups. The starter code already has the variables `price` and `quantity`.

1. Create a variable called `total` that holds `price` multiplied by `quantity`.
2. Print `total`.

Use the variables rather than typing the answer yourself. That way the program still works if the price changes.

## Recap

- `name = value` creates (or updates) a variable.
- A variable can hold the result of a calculation.
- Use `*` to multiply and `+`, `-`, `/` for the other basic operations.

## Common mistakes

- **Using a variable before creating it:** `print(total)` before `total = ...` fails with `NameError`.
- **Spelling or capitalisation differences:** `Total` and `total` are different names.
- **Putting the value on the left:** `5 = x` is a `SyntaxError`. The name always goes on the left.
