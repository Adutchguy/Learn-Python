# Cleaning Messy Data

*Optional track: Data Analysis · about 24 minutes*

> This lesson uses numpy, pandas. Install them once with `pip install -r requirements-tracks.txt`.

## Why this matters

Real data is messy: stray spaces, inconsistent capitals, prices stored as text like `"$1,200"`, blank cells, the same person entered twice. Analysts spend much of their time **cleaning** data, because wrong inputs give wrong answers however good your analysis is.

## The idea

**Missing values** appear as `NaN` ("not a number"). Find them, drop them, or fill them:

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({"name": ["Ada", "Bo", "Cy"], "score": [90.0, np.nan, 70.0]})

df["score"].isna()                          # False, True, False
df.dropna(subset=["score"])                 # remove rows missing a score
df["score"].fillna(df["score"].mean())      # replace NaN with the average (80.0)
df["score"].fillna(0)                       # or with a fixed value
```

Note that `mean()` skips `NaN` automatically.

**Text columns** have a `.str` accessor that applies string methods to every row:

```python
names = pd.Series(["  ada ", "BO", "cy"])
names.str.strip().str.title()               # Ada, Bo, Cy
names.str.lower()
names.str.contains("a")
```

**Converting types.** A column of prices stored as text cannot be added up. Strip the symbols, then convert:

```python
prices = pd.Series(["$1,200", "$35.50"])
prices.str.replace("[$,]", "", regex=True).astype(float)    # 1200.0, 35.5
```

**Duplicates:**

```python
df.drop_duplicates()                        # whole identical rows
df.drop_duplicates(subset=["name"])         # same name = same person; keep the first
```

Good habit: do cleaning in small, named steps and **return a new table** rather than changing the original, so you can always compare before and after.

## Try it

Create a Series of three messy names with spaces and mixed capitals. Clean it with `.str.strip().str.title()`. Then make a number column with one `np.nan` and fill it with the column mean.

## Your turn

Write four functions. None may change the table that was passed in.

- `clean_names(df)`: a table whose `name` column has no surrounding spaces and is in Title Case.
- `parse_prices(df)`: a table whose `price` column (text like `"$1,200.50"`) becomes floats.
- `fill_missing_scores(df)`: a table where missing `score` values are replaced by the mean of the scores that are present.
- `unique_people(df)`: a table with only the first row for each `name`, row numbers starting again from 0.

## Recap

- `isna`, `dropna` and `fillna` find, remove and replace missing values.
- `.str.` methods clean text a whole column at a time.
- `.astype(float)` converts a cleaned column to numbers.
- `drop_duplicates(subset=...)` removes repeats of the same record.

## Common mistakes

- **Comparing with `== np.nan`.** NaN is never equal to anything, even itself; use `isna()`.
- **Converting before cleaning:** `"$5".astype(float)` fails. Remove the symbols first.
- **Cleaning the original in place** and losing the raw data. Work on a copy.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/11-data-analysis/05-cleaning-messy-data
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

clean_names: the .str accessor applies string methods to a whole column: df["name"].str.strip().str.title(). Make a copy first (df = df.copy()) or use df.assign(name=...), so the table you were given is not changed.

</details>

<details><summary>Hint 2</summary>

parse_prices: .str.replace("[$,]", "", regex=True) removes the dollar sign and commas, then .astype(float) turns the text into numbers. fill_missing_scores: df["score"].fillna(df["score"].mean()) replaces each missing value with the average of the known ones.

</details>

<details><summary>Hint 3</summary>

drop_incomplete: df.dropna(subset=["score"]) removes rows where score is missing. unique_people: df.drop_duplicates(subset=["name"]) keeps the first row for each name. Add .reset_index(drop=True) when the row numbers matter.

</details>
