---
title: "Tuples and Unpacking"
minutes: 15
prereqs: ["03-data-structures/04-sorting"]
concepts: ["tuple", "immutable", "unpacking", "zip", "swap"]
local_only: false
hints:
  - "Loop over two lists at once with for name, score in zip(names, scores):. Remember to turn each score into a whole number with int()."
  - "Build the pairs as (score, name) tuples: pairs = list(zip(scores, names)). The biggest tuple is the one with the highest score, because tuples compare left to right."
  - "best_score, best_name = max(pairs) unpacks the winner into two variables. Then print(f\"Best: {best_name} ({best_score})\")."
---

## Why this matters

Sometimes two or three values belong together: a name and a score, an x and a y. A **tuple** groups them. It looks like a list but uses round brackets, and it cannot be changed after it is made. That makes it a safe way to say "these values travel together".

## The idea

```python
point = (3, 4)
print(point[0])      # 3
x, y = point         # unpacking: x is 3, y is 4
```

**Unpacking** copies the items of a tuple (or list) into separate variables in one line. It also gives Python's neat swap:

```python
a, b = 1, 2
a, b = b, a          # now a is 2 and b is 1
```

`zip` walks through several lists in step, handing you a tuple at each position:

```python
names = ["Ada", "Bo"]
ages = [36, 41]
for name, age in zip(names, ages):
    print(name, age)
```

Tuples compare item by item from the left, so `(90, "Bo") > (85, "Ada")` is `True`. That makes `max()` on a list of `(score, name)` pairs pick the highest score.

## Try it

Unpack `(1, 2, 3)` into `a, b, c`. Then try `point[0] = 9` on the tuple above and read the `TypeError`.

## Your turn

The starter reads two lines: names (words) and scores (whole numbers), in the same order. Do two things:

1. Print one line per person, like `Ada: 90`.
2. Then print who scored highest, like `Best: Ada (90)`.

For the input `Ada Bo Cy` and `90 85 70` the output is:

```text
Ada: 90
Bo: 85
Cy: 70
Best: Ada (90)
```

(The checks never contain a tie for the top score.)

## Recap

- A tuple `(a, b)` is a fixed group of values; lists use `[]` and can change, tuples cannot.
- Unpacking `x, y = point` splits a group into variables; `zip` pairs up lists.
- Tuples compare left to right, so `max` of `(score, name)` pairs finds the top score.

## Common mistakes

- **Trying to change a tuple:** `TypeError: 'tuple' object does not support item assignment`. Build a new one instead.
- **Unpacking the wrong number of items:** `ValueError: too many values to unpack`.
- **Forgetting the comma in a one-item tuple:** `(5,)` is a tuple, `(5)` is just the number 5.
