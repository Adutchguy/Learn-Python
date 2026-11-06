# CSV Files: Tables as Text

*Text and Files · about 18 minutes*

## Why this matters

**CSV** (comma-separated values) is the everyday format for tables: spreadsheets, exports from banks and shops, datasets. It is just text, one row per line, with commas between the cells. Python's `csv` module reads and writes it correctly, including the awkward cases like a comma inside a cell.

## The idea

A file `scores.csv`:

```text
name,score
Ada,90
Bo,85
```

Read it with `DictReader`, which uses the header row as the keys:

```python
import csv

with open("scores.csv", newline="") as file:
    for row in csv.DictReader(file):
        print(row["name"], row["score"])   # every value is TEXT: "90", not 90
```

Write it with `DictWriter`:

```python
with open("out.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "score"])
    writer.writeheader()
    writer.writerow({"name": "Ada", "score": 90})
```

Two details to remember:

- Open CSV files with **`newline=""`** so the module controls line endings.
- Everything read from a CSV is a **string**. Convert numbers with `int()` or `float()`.

There is also `csv.reader` / `csv.writer` which use plain lists instead of dictionaries.

## Try it

Create a small CSV file with `write_text`, read it with `DictReader`, and print the average of a numeric column.

## Your turn

The checks give your functions CSV files with a `name,score` header. Write three functions:

- `load_students(path)`: a list of `(name, score)` tuples with the score as an `int`.
- `class_average(path)`: the average score as a number.
- `save_passed(source, destination, minimum)`: write a new CSV (with the same `name,score` header) containing only the students whose score is **at least** `minimum`.

## Recap

- `csv.DictReader` gives each row as a dict keyed by the header; `DictWriter` writes dicts.
- Open CSV files with `newline=""`; values come in as text.
- Convert, filter and write back: the heart of simple data processing.

## Common mistakes

- **Doing maths on strings:** `"90" + "85"` is `"9085"`. Convert first.
- **Forgetting `writeheader()`**, so the file has no header row.
- **Splitting lines by hand** with `.split(",")`: it breaks on quoted commas. Use `csv`.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/05-text-and-files/04-csv-files
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

load_students: open the file with newline="", make csv.DictReader(file), and for each row build (row["name"], int(row["score"])). Scores arrive as text, so convert them.

</details>

<details><summary>Hint 2</summary>

class_average: reuse load_students(path), take the scores, and return their sum divided by how many there are.

</details>

<details><summary>Hint 3</summary>

save_passed: open the destination with "w" and newline="", create csv.DictWriter(file, fieldnames=["name", "score"]), call writeheader(), then writerow({"name": name, "score": score}) for each student at or above the minimum.

</details>
