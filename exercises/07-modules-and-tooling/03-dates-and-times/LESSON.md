# Dates and Times

*Modules and Tooling · about 18 minutes*

## Why this matters

Dates look easy until you meet leap years, month lengths and weekends. The `datetime` module does the hard parts, so you never count days by hand.

## The idea

```python
from datetime import date, datetime, timedelta

d = date(2024, 3, 5)                  # year, month, day
d.year, d.month, d.day                # 2024 3 5
d.weekday()                           # 1  (Monday is 0, Sunday is 6)
d + timedelta(days=30)                # date(2024, 4, 4)
date(2024, 12, 25) - d                # timedelta(days=295)
(date(2024, 12, 25) - d).days         # 295

d.strftime("%d %B %Y")                # '05 March 2024'  (date -> text)
datetime.strptime("2024-03-05", "%Y-%m-%d").date()   # text -> date
```

Common format codes: `%Y` year, `%m` month number, `%d` day, `%B` month name, `%A` weekday name, `%H:%M` hours and minutes. `date.today()` gives today's date, but functions that take the date as a parameter are much easier to test.

## Try it

Work out how many days there are from today until the end of the year. Then print today's weekday name with `strftime("%A")`.

## Your turn

Write four functions:

- `days_until(today, target)`: the number of days from `today` to `target`, both `date` objects. It is negative when `target` is in the past.
- `format_date(d)`: text like `05 March 2024`.
- `parse_date(text)`: turn `"2024-03-05"` into a `date`. Other formats raise `ValueError`.
- `add_business_days(start, n)`: the date `n` business days after `start`, skipping Saturdays and Sundays. From Friday 8 March 2024, one business day later is Monday 11 March.

## Recap

- `date` holds a day, `timedelta` a length of time; subtract dates to get a `timedelta`.
- `strftime` formats a date as text; `strptime` parses text into a date.
- Pass dates into functions instead of calling `date.today()` inside, so they can be tested.

## Common mistakes

- **Mixing up `date` and `datetime`**: `TypeError: can't compare datetime.datetime to datetime.date`.
- **Wrong format codes** (`%m` is the month number, `%M` is minutes), which raise `ValueError` when parsing.
- **Forgetting that Monday is 0**, so weekdays are 0 to 4.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/07-modules-and-tooling/03-dates-and-times
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

days_until: subtracting two dates gives a timedelta; its .days attribute is the whole number of days: (target - today).days. format_date: d.strftime("%d %B %Y").

</details>

<details><summary>Hint 2</summary>

parse_date: from datetime import datetime; datetime.strptime(text, "%Y-%m-%d").date(). A text that does not match the format raises ValueError by itself; you do not need to catch it.

</details>

<details><summary>Hint 3</summary>

add_business_days: current = start; while n > 0: current += timedelta(days=1); and only when current.weekday() < 5 (Monday is 0, Friday is 4) do n -= 1. Return current.

</details>
