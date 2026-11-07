---
title: "pandas: Tables of Data with DataFrames"
minutes: 22
prereqs: ["11-data-analysis/01-numpy-arrays"]
concepts: ["pandas", "DataFrame", "Series", "columns", "idxmax", "assign", "describe"]
local_only: false
packages: ["numpy", "pandas"]
hints:
  - "build_scores: pd.DataFrame({\"name\": names, \"points\": points}) builds the table from a dict of columns."
  - "top_scorer: df[\"points\"].idxmax() gives the row label of the largest value; df.loc[label, \"name\"] reads a cell. add_bonus: return df.assign(total=df[\"points\"] + bonus); assign gives back a new table and leaves df alone."
  - "describe_points: df[\"points\"] is a Series, which has .mean(), .max() and .min(). Wrap each in float(...) so the numbers are plain Python floats: {\"mean\": float(...), \"max\": float(...), \"min\": float(...)}."
---

## Why this matters

Most real data is a **table**: rows of records and columns of facts, like a spreadsheet or a CSV file. **pandas** is Python's standard tool for working with tables. Its main object, the **DataFrame**, lets you ask questions of a whole table in a line or two: totals, averages, filters, groupings.

## The idea

A DataFrame is a table with named columns. Each column is a **Series** (a labelled array, like a NumPy array with an index).

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ada", "Bo", "Cy"],
    "points": [30, 45, 38],
})
print(df)
#   name  points
# 0  Ada      30
# 1   Bo      45
# 2   Cy      38
```

The numbers on the left are the **index** (row labels). You get a column with `df["points"]`, and calculations on it work on every row at once:

```python
df["points"].mean()            # 37.666666666666664
df["points"].max()             # 45
df["points"] * 2               # a Series: 60, 90, 76
```

Find the row of the biggest value, then read a cell with `.loc[row_label, column_name]`:

```python
best = df["points"].idxmax()   # 1
df.loc[best, "name"]           # 'Bo'
```

To add a column **without changing the original table**, use `assign`, which returns a new DataFrame:

```python
with_bonus = df.assign(total=df["points"] + 5)
```

Handy first looks at a table: `df.head()` (first rows), `df.shape` (rows, columns), `df.columns`, `df.describe()` (summary statistics).

## Try it

Make a DataFrame of three of your friends with a number column such as age. Print `df.describe()`, then print the column with the biggest value using `idxmax`.

## Your turn

Write four functions:

- `build_scores(names, points)`: a DataFrame with the columns `"name"` and `"points"`.
- `top_scorer(df)`: the name of the person with the most points.
- `add_bonus(df, bonus)`: a **new** DataFrame with an extra column `"total"` equal to `points + bonus`. The original must not change.
- `describe_points(df)`: a dict with the `"mean"`, `"max"` and `"min"` of the points column, as plain floats.

## Recap

- A DataFrame is a table; each column is a Series.
- `df["col"]` selects a column; arithmetic and methods like `.mean()` apply to all its rows.
- `idxmax()` finds *where* the biggest value is; `.loc[row, column]` reads a cell.
- `assign` adds a column and returns a new table, leaving the original untouched.

## Common mistakes

- **Looping over rows** to add things up. Use the column operation (`df["points"].sum()`).
- **Forgetting that `idxmax` returns a label**, not the value itself. Use `.loc` to read the cell.
- **Expecting a method to change the table in place.** Most pandas methods return a new object; keep it with `df = df.assign(...)`.
