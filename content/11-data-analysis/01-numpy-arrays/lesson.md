---
title: "NumPy Arrays: Maths on Whole Lists at Once"
minutes: 20
prereqs: ["03-data-structures/08-comprehensions"]
concepts: ["numpy", "array", "vectorised operations", "boolean mask", "shape", "axis", "mean"]
local_only: false
packages: ["numpy"]
hints:
  - "celsius_to_fahrenheit: put the values in an array with np.array(temps) and use ordinary arithmetic on the whole array: array * 9 / 5 + 32. No loop is needed."
  - "normalise: low = values.min() and high = values.max(); then (values - low) / (high - low). above_average: a comparison on the whole array, values > values.mean(), gives a True/False array; index with it: values[values > values.mean()]."
  - "column_means: grid = np.array(rows) makes a 2D array. grid.mean(axis=0) averages down each column (axis=1 would average across each row)."
---

## Why this matters

Data work means doing the same calculation on thousands or millions of numbers. A Python `for` loop over a list is slow and wordy for that. **NumPy** gives you an **array**: a fixed-type grid of numbers where one expression works on every element at once. It is the base that pandas, machine-learning libraries and scientific code are built on.

## The idea

```python
import numpy as np

prices = np.array([4.0, 10.0, 6.5])
print(prices * 2)          # [ 8.  20.  13. ]   every element doubled
print(prices + prices)     # [ 8.  20.  13. ]   element by element
print(prices.mean())       # 6.833333333333333
print(prices.max())        # 10.0
```

Arithmetic on an array applies to every element (this is called **vectorising**). Compare with a plain list, where `[1, 2] * 2` repeats the list instead.

**Comparisons give a mask** of `True`/`False`, and a mask picks out elements:

```python
prices > 5                 # [False  True  True]
prices[prices > 5]         # [10.   6.5]
```

**Shape and axis.** A list of lists becomes a 2D array. `shape` tells you its size, and `axis` says which direction a calculation runs:

```python
grid = np.array([[1, 2, 3],
                 [4, 5, 6]])
grid.shape                 # (2, 3): 2 rows, 3 columns
grid.mean(axis=0)          # [2.5 3.5 4.5]   one result per column
grid.mean(axis=1)          # [2. 5.]         one result per row
```

Other handy tools: `np.arange(5)` (like `range`, but an array), `np.zeros(3)`, `np.round(x, 2)` and `np.sum`.

## Try it

Make an array of five numbers. Multiply it by 10, take its `.mean()`, and use a mask to keep only the values greater than the mean.

## Your turn

Write four functions. Each should return a NumPy array and avoid loops:

- `celsius_to_fahrenheit(temps)`: convert a list of Celsius temperatures (F = C × 9 / 5 + 32).
- `normalise(values)`: rescale a list so the smallest becomes 0 and the largest becomes 1: `(x - min) / (max - min)`.
- `above_average(values)`: only the values greater than the average of all of them.
- `column_means(rows)`: the average of each column of a list of equal-length rows.

## Recap

- An array applies arithmetic to every element at once; no loop needed.
- A comparison gives a True/False mask, and `array[mask]` keeps the matching elements.
- `shape` is the size; `axis=0` works down columns and `axis=1` across rows.
- Arrays hold one type of number, which is what makes them fast.

## Common mistakes

- **Expecting list behaviour:** `[1, 2] * 2` repeats the list, while `np.array([1, 2]) * 2` doubles the numbers.
- **Mixing up the axes:** `axis=0` collapses the rows, leaving one value per column.
- **Writing a loop anyway.** If you are looping over an array, there is usually a one-line array expression instead.
