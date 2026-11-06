---
title: "Project: An Expense Tracker"
minutes: 40
prereqs: ["06-errors-and-debugging/05-context-managers"]
concepts: ["project", "try/except", "raise", "files", "dictionaries", "formatting", "error handling"]
local_only: false
hints:
  - "parse_expense: parts = line.split(); if len(parts) != 2: raise ValueError(\"expected CATEGORY AMOUNT, for example: food 12.50\"). Convert parts[1] with float() inside try/except ValueError and raise ValueError(\"amount must be a number\") from the except block. Then raise ValueError(\"amount must be positive\") if amount <= 0. Return (parts[0].lower(), amount)."
  - "load_expenses: try: open the file and read its lines; except FileNotFoundError: return []. For each line use category, _, amount = line.partition(\",\") and add (category, float(amount)) inside try/except ValueError: continue. save_expense opens the file with mode \"a\" and writes f\"{category},{amount}\\n\"."
  - "totals_by_category: totals[category] = totals.get(category, 0) + amount, then round each total to 2 decimals. format_report: return \"No expenses yet.\" if empty; sort with sorted(totals.items(), key=lambda item: (-item[1], item[0])); each line is f\"{category:<10}{amount:>8.2f}\"; finish with the same layout using the word total."
---

## Why this matters

Time for a second project. This **expense tracker** is a small command-line program that reads commands, rejects bad input politely, stores data in a file and prints a report. It brings together exactly what this module taught: catching errors, raising your own, and keeping a program running when things go wrong.

## The idea

The main program is already written at the bottom of the starter. You write the five functions it relies on:

| Function | Job |
|---|---|
| `parse_expense(line)` | turn `"food 12.50"` into `("food", 12.5)` or raise `ValueError` |
| `load_expenses(path)` | read saved expenses; no file yet means an empty list |
| `save_expense(path, category, amount)` | append one line to the file |
| `totals_by_category(expenses)` | add up the amounts for each category |
| `format_report(totals)` | build the printed report |

Each stored line looks like `food,12.5`. The main program turns your `ValueError` into a friendly `Error: ...` line instead of crashing.

## Try it

Read the `main()` function first. Trace what happens for the commands `add food 12.5`, then `add food`, then `report`. Which of your functions runs each time?

## Your turn

Complete the five functions. The error messages and layouts below are exact, because the checks compare them.

**`parse_expense`** splits the line on spaces. It lower-cases the category and returns the amount as a float. It raises `ValueError` with exactly these messages:

- wrong number of parts: `expected CATEGORY AMOUNT, for example: food 12.50`
- amount is not a number: `amount must be a number`
- amount is zero or less: `amount must be positive`

**`load_expenses`** returns a list of `(category, amount)` tuples. A missing file gives `[]`. Blank or broken lines are skipped.

**`totals_by_category`** returns a dictionary of category to total, each rounded to 2 decimals.

**`format_report`** returns `No expenses yet.` for an empty dictionary. Otherwise one line per category, biggest amount first (ties by name), then a total line. Each line is the category padded to 10 characters followed by the amount right-aligned in 8 characters with 2 decimals:

```text
rent        500.00
food         12.50
total       512.50
```

## Recap

- Validate input in one place and `raise` clear errors; handle them in the caller.
- A missing file is often a normal situation, not a crash.
- Small functions that each do one job are easy to test and reuse.

## Common mistakes

- **Catching `Exception` in `main`** instead of the specific `ValueError`, which would hide real bugs.
- **Opening the save file with `"w"`**, which wipes earlier expenses. Use `"a"` to append.
- **Forgetting to lower-case the category**, so `Food` and `food` are totalled separately.
