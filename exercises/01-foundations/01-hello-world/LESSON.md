# Hello, World!

*Foundations · about 10 minutes*

## Why this matters

Every program needs a way to *show* something to a person. In Python, the simplest way is `print()`.

## The idea

`print()` is a **function**: a named action that Python already knows how to do. You hand it something inside the parentheses, and it shows that something on the screen.

```python
print("Hello, world")
```

The text between the quotes is called a **string**. Python prints what is *inside* the quotes, without the quotes themselves. Single quotes work too: `'Hello'` and `"Hello"` mean the same thing.

Each `print()` ends by moving to a new line, so two prints show two lines:

```python
print("First line")
print("Second line")
```

## Try it

In the editor below, change the text inside the quotes and press **Run**. Break something on purpose, too (delete a quote, for example) and read the error message. Errors are not failures; they are Python telling you exactly what it did not understand.

## Your turn

The starter program prints `Hello, world`. Change it so that it prints exactly:

```
Hello, Python!
```

Press **Run** to see your output, then **Check** to test your answer.

## Recap

- `print()` shows something on the screen.
- Text in quotes is a string.
- Each `print()` call produces its own line.

## Common mistakes

- **Forgetting the quotes:** `print(Hello)` fails with `NameError`, because Python thinks `Hello` is the name of something it should already know.
- **Missing parenthesis:** `print("Hello"` fails with `SyntaxError`.
- **Wrong capitalisation:** Python is case-sensitive. `Print("Hi")` fails with `NameError`.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/01-foundations/01-hello-world
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Look at the line that is already in the editor. Which part of it is different from the greeting you are asked to print?

</details>

<details><summary>Hint 2</summary>

The text you want printed goes between the quotes, inside the parentheses of print().

</details>

<details><summary>Hint 3</summary>

Change the text so it reads exactly: Hello, Python!  Capital H, capital P, a comma, and an exclamation mark.

</details>
