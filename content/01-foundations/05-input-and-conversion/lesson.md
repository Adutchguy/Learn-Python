---
title: Asking for Input and Converting Types
minutes: 15
prereqs: ["01-foundations/04-data-types"]
concepts: [input, int(), float(), str(), type conversion]
local_only: false
hints:
  - "Start with: age = int(input(\"Your age: \")). input() always gives you text, so int() turns it into a number."
  - "Next year's age is age + 1."
  - "Finish with: print(\"Next year you will be\", age + 1)"
---

## Why this matters

Programs become useful when they respond to a person. The built-in `input()` pauses the program, lets the user type something, and hands it back to you.

## The idea

```python
name = input("What is your name? ")
print("Hello,", name)
```

The text inside `input()` is the **prompt** shown to the user. Whatever they type becomes the value.

There is one catch that trips up almost everyone: **`input()` always gives you text** (a `str`), even if the user types a number.

```python
age = input("Age: ")       # the user types 30
print(age + 1)             # TypeError: can only concatenate str (not "int") to str
```

`"30"` is text, and you cannot add `1` to text. Convert it first with:

- `int(...)`: text or float → whole number: `int("30")` is `30`
- `float(...)`: text or int → decimal number: `float("2.5")` is `2.5`
- `str(...)`: anything → text: `str(30)` is `"30"`

```python
age = int(input("Age: "))
print(age + 1)             # works: 31
```

`int("abc")` or `int("2.5")` raises a `ValueError`. That is Python telling you the text is not a whole number.

## Try it

When your program asks for input, type your answer in the **Input box** under the editor *before* pressing Run (one line for each `input()` call). Try the example above with `age = int(input(...))`, then try it with a plain `input()` and see the `TypeError`.

## Your turn

Write a program that asks for the user's age and prints how old they will be next year. If the user types `30`, it must print exactly:

```text
Next year you will be 31
```

Use `input()` and `int()`. Remember to type a number in the Input box before you press Run. **Check** will try several ages for you.

## Recap

- `input("prompt")` reads what the user types, as text.
- Convert with `int()`, `float()` or `str()` before doing maths.
- Putting the conversion right around the `input()` is the usual pattern: `int(input(...))`.

## Common mistakes

- **Forgetting to convert:** `age + 1` fails with a `TypeError` while `age` is text.
- **Typing nothing in the Input box** (in the browser). Your program will stop with an `EOFError` that says so.
- **Converting too early or too late.** Convert once, right when you read the value.
