---
title: "Project: Analyse a Sales Dataset"
minutes: 35
prereqs: ["11-data-analysis/05-cleaning-messy-data"]
concepts: ["read_csv", "StringIO", "to_datetime", "dt accessor", "groupby", "nlargest", "report", "data analysis project"]
local_only: false
packages: ["numpy", "pandas"]
hints:
  - "load_sales: pd.read_csv(io.StringIO(csv_text)) reads the text as if it were a file. Then df.dropna(subset=[\"units\"]), convert dates with pd.to_datetime(df[\"date\"]), and add revenue with assign(revenue=df[\"units\"] * df[\"price\"]). Use .reset_index(drop=True) at the end."
  - "revenue_by_month: df[\"date\"].dt.strftime(\"%Y-%m\") turns each date into a month label. Group revenue by that, sum, round to 2, and return .to_dict(); a groupby result is already in month order."
  - "best_products: df.groupby(\"product\")[\"revenue\"].sum().nlargest(n) gives the top n. Turn it into a list of (product, revenue) pairs with [(p, round(float(r), 2)) for p, r in series.items()]. report: build the three lines with f-strings and join them with \"\\n\"."
---

## Why this matters

You now have every piece of a data analysis: load a table, clean it, filter it, group it and summarise it. This project puts them together into a small report, the same shape as a real analysis for a small shop.

## The idea

You get a sales log as CSV text (the kind of file a till or spreadsheet exports):

```text
date,product,units,price
2026-01-05,tea,10,2.50
2026-01-20,coffee,4,3.00
2026-02-03,tea,,2.50
```

One row has no `units`, so it is not a real sale. The plan:

1. **Load and clean:** read the CSV, drop rows with no `units`, convert `date` to real dates and add a `revenue` column (`units * price`).
2. **Monthly revenue:** total revenue per month, as a dict like `{"2026-01": 49.0, ...}`.
3. **Best products:** the top `n` products by total revenue.
4. **Report:** three readable lines.

Two tools you have not used yet:

```python
import io
import pandas as pd

df = pd.read_csv(io.StringIO(csv_text))      # read CSV from a string instead of a file
df["date"] = pd.to_datetime(df["date"])       # text -> real dates
df["date"].dt.strftime("%Y-%m")               # "2026-01": the date as text in your format
series.nlargest(3)                            # the 3 biggest values
```

`io.StringIO` wraps a string so pandas can read it like a file. That keeps this project self-contained, and the same code works on a real file: `pd.read_csv("sales.csv")`.

## Try it

Make a small CSV string, load it with `read_csv(io.StringIO(...))`, and print `df.info()` to see the columns and their types.

## Your turn

Write these four functions:

- `load_sales(csv_text)`: the cleaned table, with columns `date` (datetime), `product`, `units`, `price`, `revenue`, and row numbers from 0.
- `revenue_by_month(df)`: a dict of `"YYYY-MM"` to total revenue rounded to 2 decimals, in month order.
- `best_products(df, n)`: a list of `(product, total revenue rounded to 2)` pairs, best first, at most `n` long.
- `report(df)`: a string of exactly three lines:
  `Total revenue: $<total, 2 decimals>`, `Best product: <name>`, `Busiest month: <YYYY-MM>` (the month with the most revenue).

## Recap

- `read_csv` + `StringIO` loads CSV text; `to_datetime` and `.dt` handle dates.
- A real analysis is a pipeline: load, clean, derive columns, group, summarise.
- Small functions that each return a simple result are easy to test and reuse.

## Going further

Try your functions on a real CSV export (a bank statement, a fitness log). Add a function for the weekday with the most sales (`df["date"].dt.day_name()`), or chart revenue by month with the next lesson.
