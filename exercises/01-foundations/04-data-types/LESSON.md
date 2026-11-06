# Values and Types

*Foundations · about 12 minutes*

## Why this matters

Python treats a number, a piece of text and a yes/no answer very differently. Knowing which **type** of value you have explains most surprising behaviour, and most `TypeError`s.

## The idea

Every value has a type. The four you will use constantly:

| Type | What it holds | Examples |
|---|---|---|
| `int` | whole numbers | `7`, `-3`, `0` |
| `float` | numbers with a decimal point | `2.5`, `-0.1`, `3.0` |
| `str` | text (a "string"), written in quotes | `"hello"`, `'Python'`, `""` |
| `bool` | yes or no | `True`, `False` |

Notice that `3` and `3.0` are **different types**, and `"3"` (text) is a third thing again. Text in quotes is always a `str`, even if it looks like a number.

The built-in `type()` function tells you what you have:

```python
print(type(42))        # <class 'int'>
print(type(2.5))       # <class 'float'>
print(type("42"))      # <class 'str'>
print(type(True))      # <class 'bool'>
```

A variable has no type of its own; it just holds a value, and that value has one:

```python
x = 5        # x holds an int
x = "five"   # now x holds a str
```

## Try it

Use `print(type(...))` on a few things: a whole number, a decimal, `"7"` in quotes, `7 / 2`, `True`. Predict each answer before pressing Run. What type is `7 / 2`?

## Your turn

In the editor, each variable currently holds `...` (a placeholder). Replace each `...` with a value of the type its comment asks for. Then, at the bottom, print the type of the value `42`.

## Recap

- Every value has a type: `int`, `float`, `str` or `bool` (and more to come).
- Quotes make text: `"7"` is a `str`, `7` is an `int`.
- `type(value)` tells you the type.

## Common mistakes

- **Putting quotes around `True`.** `"True"` is text; `True` is a `bool`.
- **Lowercase `true`.** Python only recognises `True` and `False`.
- **Mixing up `3` and `"3"`.** They look similar but behave differently, as you will see when you use `+`.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/01-foundations/04-data-types
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Replace each ... with a real value. A whole number like 7 is an int; a number with a decimal point like 2.5 is a float.

</details>

<details><summary>Hint 2</summary>

A str is text in quotes, like "hello". A bool is exactly True or False, with a capital first letter and no quotes.

</details>

<details><summary>Hint 3</summary>

For the last part, write: print(type(42))

</details>
