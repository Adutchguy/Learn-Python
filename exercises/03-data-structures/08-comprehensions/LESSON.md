# Comprehensions: Building Collections in One Line

*Data Structures · about 15 minutes*

## Why this matters

A very common loop builds a new list from an old one: double every price, keep only the big ones. A **comprehension** says the same thing in a single readable line. You will see them everywhere in real Python code.

## The idea

The loop you already know:

```python
squares = []
for n in [1, 2, 3, 4]:
    squares.append(n * n)
```

The comprehension that does the same:

```python
squares = [n * n for n in [1, 2, 3, 4]]   # [1, 4, 9, 16]
```

Read it as: "`n * n` for each `n` in the list". Add an `if` to filter:

```python
big = [n for n in [1, 5, 8, 2] if n > 4]  # [5, 8]
```

The same shape builds other collections:

```python
lengths = {w: len(w) for w in ["hi", "hello"]}  # {'hi': 2, 'hello': 5}
unique = {n % 3 for n in range(10)}             # {0, 1, 2}
```

Use a comprehension when it fits on one line and stays easy to read. If it gets complicated, a normal loop is kinder to the next reader (that includes you).

## Try it

Write a comprehension that makes upper-case versions of `["a", "b", "c"]`. Then one that keeps only the words longer than 3 letters from `["tree", "sun", "forest"]`.

## Your turn

The starter reads some numbers and some words. Using comprehensions, print two lines. For numbers `1 2 3 4` and words `cat horse`:

```text
Even squares: [4, 16]
Lengths: {'cat': 3, 'horse': 5}
```

"Even squares" is the square of each even number, in the original order. "Lengths" maps each word to its length (words in the order given).

## Recap

- `[expression for item in items if condition]` builds a new list in one line.
- Curly braces with `key: value` make a dict; without it they make a set.
- Prefer a plain loop when the comprehension stops being easy to read.

## Common mistakes

- **Putting the `if` in the wrong place.** A filter goes at the end: `[n for n in nums if n > 0]`.
- **Side effects inside a comprehension**, such as printing. Build the collection, then use it.
- **Over-clever one-liners.** Clear beats short.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/03-data-structures/08-comprehensions
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

A list comprehension has the shape [expression for item in items if condition]. For the squares you want number * number for numbers that are even.

</details>

<details><summary>Hint 2</summary>

even_squares = [n * n for n in numbers if n % 2 == 0]. Print it with print(f"Even squares: {even_squares}").

</details>

<details><summary>Hint 3</summary>

A dictionary comprehension is {word: len(word) for word in words}. Print it the same way: print(f"Lengths: {lengths}").

</details>
