---
title: "Comprehension Patterns and Generator Expressions"
minutes: 16
prereqs: ["09-pythonic-python/02-generators"]
concepts: ["nested comprehensions", "dict comprehension", "set comprehension", "generator expression", "conditional expression", "all/any"]
local_only: false
hints:
  - "flatten is a comprehension with two for parts, in reading order: [item for row in matrix for item in row]. invert is {value: key for key, value in d.items()}. unique_lengths is the same idea with set braces and len(word)."
  - "label_parity uses a conditional expression inside the comprehension: [\"even\" if n % 2 == 0 else \"odd\" for n in numbers]. The if/else goes BEFORE the for here."
  - "all_positive and any_long take a generator expression inside all()/any(): all(n > 0 for n in numbers). No square brackets: a list would read every item first, but a generator lets all() stop at the first False."
---

## Why this matters

You already know list comprehensions. The same idea builds dictionaries and sets, handles nested loops, and, with round brackets, becomes a lazy **generator expression** that never builds the whole list. These patterns replace many small loops.

## The idea

```python
nums = [1, 2, 3, 4]

[n * n for n in nums]                 # list:  [1, 4, 9, 16]
{n % 2 for n in nums}                 # set:   {0, 1}
{n: n * n for n in nums}              # dict:  {1: 1, 2: 4, 3: 9, 4: 16}
```

Two `for` parts read left to right, like nested loops:

```python
grid = [[1, 2], [3, 4]]
[cell for row in grid for cell in row]    # [1, 2, 3, 4]
```

To choose between two values, use a **conditional expression** (`A if test else B`). It goes in front of the `for`. A filter `if` goes after:

```python
["even" if n % 2 == 0 else "odd" for n in nums]   # choose a value
[n for n in nums if n % 2 == 0]                   # filter items
```

Round brackets give a **generator expression**. It produces values on demand, which is perfect inside `sum`, `max`, `all` and `any`:

```python
sum(n * n for n in nums)              # 30, no list built
any(n > 3 for n in nums)              # True, stops at 4
```

If a comprehension gets hard to read, use a normal loop. Clear beats clever.

## Try it

Run the examples. Then make a dict that maps each word in `["apple", "fig"]` to its length.

## Your turn

Write these functions, each as a one-line comprehension or generator expression:

- `flatten(matrix)`: all items of a list of lists, as one list.
- `invert(d)`: swap keys and values of a dictionary.
- `unique_lengths(words)`: the **set** of word lengths.
- `label_parity(numbers)`: `"even"` or `"odd"` for each number.
- `all_positive(numbers)`: `True` if every number is above 0. Use `all()` with a generator expression, so it stops at the first number that is not.
- `any_long(words, size)`: `True` if any word has at least `size` letters (also lazy).

## Recap

- `{k: v for ...}` builds a dict; `{x for ...}` builds a set.
- Several `for` parts read like nested loops, outer first.
- `A if test else B` picks a value; a trailing `if` filters.
- A generator expression in `all`/`any`/`sum` is lazy and can stop early.

## Common mistakes

- **Putting `if/else` after the `for`**: a value choice goes before it, a filter goes after.
- **Using `[...]` inside `all()`** and losing the early stop.
- **Cramming too much** into one comprehension. Split it into a loop when it is hard to read.
