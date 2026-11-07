---
title: "Grouping and Summarising"
minutes: 22
prereqs: ["11-data-analysis/03-selecting-and-filtering"]
concepts: ["groupby", "sum", "mean", "agg", "value_counts", "reset_index", "split-apply-combine"]
local_only: false
packages: ["numpy", "pandas"]
hints:
  - "total_by_category: df.groupby(\"category\")[\"amount\"].sum() gives a Series indexed by category. Turn it into a plain dict with .to_dict(); wrap values with float() if you want plain floats."
  - "average_by: df.groupby(key)[value].mean().round(2).to_dict(). busiest_category: df[\"category\"].value_counts() counts the rows per category, biggest first, so .idxmax() or .index[0] is the answer."
  - "summary_table: df.groupby(\"category\").agg(count=(\"amount\", \"count\"), mean=(\"amount\", \"mean\")).reset_index() builds a table with one row per category. Use .round(2) on the result so the means are tidy."
---

## Why this matters

"Total spending *per category*." "Average score *per team*." Questions with "per" in them are **grouping** questions, and they are the heart of data analysis. pandas does them with `groupby`: split the table into groups, calculate something for each group, and combine the answers.

## The idea

```python
import pandas as pd

spending = pd.DataFrame({
    "category": ["food", "travel", "food", "fun", "travel"],
    "amount":   [12.5,   40.0,     7.5,    20.0,  10.0],
})

totals = spending.groupby("category")["amount"].sum()
print(totals)
# category
# food      20.0
# fun       20.0
# travel    50.0
# Name: amount, dtype: float64
```

Read it left to right: *group the rows by category, take the amount column, add each group up*. Other summaries work the same way: `.mean()`, `.max()`, `.min()`, `.count()`, `.size()`.

```python
totals.to_dict()          # {'food': 20.0, 'fun': 20.0, 'travel': 50.0}
totals.idxmax()           # 'travel'  (the label of the biggest total)
```

**Counting how often each value appears:**

```python
spending["category"].value_counts()    # travel 2, food 2, fun 1 (biggest first)
```

**Several summaries at once** with `agg`. Each keyword is a new column: `name=("column", "function")`:

```python
table = spending.groupby("category").agg(
    count=("amount", "count"),
    mean=("amount", "mean"),
).reset_index()
```

`reset_index()` turns the group names from the index back into an ordinary column, which makes the result an easy-to-read table.

## Try it

Group the table above by `category` and find the `.mean()` of `amount` for each. Then add `.round(1)` to tidy the numbers.

## Your turn

The functions receive a table with `category` and `amount` columns (`summary_table` also works with any such table). Write:

- `total_by_category(df)`: a dict of category to total amount.
- `average_by(df, key, value)`: a dict of each `key` group to the average of the `value` column, rounded to 2 decimals.
- `busiest_category(df)`: the category that appears in the most rows.
- `summary_table(df)`: a table with one row per category and the columns `category`, `count` and `mean` (the mean rounded to 2 decimals), in alphabetical order of category.

## Recap

- `df.groupby("col")["other"].sum()` answers "per group" questions.
- Summaries: `sum`, `mean`, `min`, `max`, `count`, `size`; `value_counts()` counts occurrences.
- `agg(name=("column", "function"))` calculates several summaries at once.
- `reset_index()` turns group labels back into a normal column.

## Common mistakes

- **Forgetting to pick a column** before the summary, so pandas tries to add up everything (including text).
- **Reading the result as a plain column.** After `groupby` the group names are the *index*; use `reset_index()` or `.to_dict()`.
- **Confusing `count` and `size`:** `count` skips missing values; `size` counts every row.
