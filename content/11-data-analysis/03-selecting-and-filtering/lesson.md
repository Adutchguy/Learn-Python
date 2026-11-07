---
title: "Selecting and Filtering Rows"
minutes: 22
prereqs: ["11-data-analysis/02-pandas-dataframes"]
concepts: ["boolean mask", "&", "|", "isin", "loc", "sort_values", "reset_index", "selecting columns"]
local_only: false
packages: ["numpy", "pandas"]
hints:
  - "adults: build a mask with df[\"age\"] >= 18 and index the table with it: df[df[\"age\"] >= 18]. names_in_city: combine two masks with & and put each comparison in parentheses: df[(df[\"age\"] >= 18) & (df[\"city\"] == city)][\"name\"].tolist()."
  - "select_columns: df[cols] with a list of names gives a table with just those columns. in_cities: df[df[\"city\"].isin(cities)] keeps rows whose city is in the list."
  - "oldest_first: df.sort_values(\"age\", ascending=False) puts the oldest on top; add .reset_index(drop=True) so the row numbers start from 0 again."
---

## Why this matters

Most questions about data start with "just the rows where...". Which customers are adults? Which orders are from Seattle? pandas answers with **boolean masks**, the same idea you met in NumPy, applied to a table.

## The idea

```python
import pandas as pd

people = pd.DataFrame({
    "name": ["Ada", "Bo", "Cy", "Di"],
    "age": [34, 17, 45, 29],
    "city": ["Rome", "Oslo", "Rome", "Oslo"],
})

mask = people["age"] >= 18          # True/False for each row
people[mask]                         # only the adults
```

Put the mask straight inside the square brackets: `people[people["age"] >= 18]`.

**Combine conditions** with `&` (and), `|` (or) and `~` (not). Unlike plain Python, each condition **must be in parentheses**, and you cannot use the words `and` / `or`:

```python
people[(people["age"] >= 18) & (people["city"] == "Rome")]
```

More tools:

```python
people[["name", "city"]]                 # choose columns (note the double brackets)
people[people["city"].isin(["Rome"])]    # value is one of a list
people.sort_values("age", ascending=False)
people.sort_values("age").reset_index(drop=True)   # renumber the rows from 0
people.loc[people["age"] > 30, "name"]   # rows by mask, one column
```

A filtered table keeps its old row numbers, which is why `reset_index(drop=True)` is useful when you want a clean 0, 1, 2, ... again.

## Try it

Build the table above. Print the people in Oslo who are over 20. Then print just their names as a list with `.tolist()`.

## Your turn

The functions receive a table with the columns `name`, `age` and `city`. Write:

- `adults(df)`: only the rows where `age` is 18 or more.
- `names_in_city(df, city)`: a list of the names of the adults in that city.
- `select_columns(df, cols)`: a table with only the named columns.
- `in_cities(df, cities)`: the rows whose city is in the list `cities`.
- `oldest_first(df)`: all rows, oldest first, with row numbers starting again from 0.

## Recap

- `df[mask]` keeps the rows where the mask is `True`.
- Join conditions with `&`, `|`, `~`, each in parentheses.
- `df[["a", "b"]]` picks columns; `isin` tests membership; `sort_values` orders rows.
- `reset_index(drop=True)` renumbers rows after filtering or sorting.

## Common mistakes

- **Using `and` / `or`** between masks. That raises an error; use `&` / `|`.
- **Forgetting the parentheses:** `df["a"] > 1 & df["b"] < 5` does the `&` first and fails.
- **Single brackets for several columns.** Use a list inside the brackets: `df[["name", "city"]]`.
