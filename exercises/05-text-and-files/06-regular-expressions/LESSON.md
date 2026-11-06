# Regular Expressions: Finding Patterns

*Text and Files · about 20 minutes*

## Why this matters

String methods work when you know exactly what to look for. But what about "any phone number", "every hashtag" or "a date in the form 2026-11-06"? A **regular expression** (regex) describes a *pattern* of text, and Python's `re` module finds, extracts and replaces every match. It is a compact language worth learning at a basic level.

## The idea

```python
import re

text = "Order 66 shipped on 2026-11-06"
re.findall(r"\d+", text)             # ['66', '2026', '11', '06']
re.search(r"\d{4}", text).group()    # '2026'  (the first match, or None)
re.sub(r"\d", "#", text)             # replace every digit with #
```

Always write patterns as **raw strings** (`r"..."`) so Python leaves the backslashes alone.

The building blocks:

| Pattern | Matches |
|---|---|
| `\d` / `\w` / `\s` | a digit / a letter, digit or underscore / whitespace |
| `.` | any one character |
| `+` / `*` / `?` | one or more / zero or more / optional |
| `{4}` | exactly four of the previous thing |
| `[abc]` / `[a-z]` | any one of those characters |
| `^` / `$` | start / end of the text |
| `( )` | a **group**: capture just that part |

With groups, `findall` returns only the captured part, and `match.groups()` gives them all:

```python
m = re.fullmatch(r"(\d{4})-(\d{2})", "2026-11")
m.groups()                             # ('2026', '11')
```

`re.fullmatch` requires the **whole** text to match; `re.search` finds a match anywhere. They return `None` when there is no match, so check before using the result.

## Try it

Use `re.findall` to pull every word that starts with a capital letter out of a sentence (`[A-Z]\w*`). Then use `re.sub` to replace runs of spaces with a single space.

## Your turn

Write three functions:

- `find_numbers(text)`: every whole number in the text, as a list of `int`s: `find_numbers("3 cats and 12 dogs")` is `[3, 12]`.
- `find_hashtags(text)`: the words after each `#`, without the `#`: `find_hashtags("I love #python and #coding!")` is `["python", "coding"]`.
- `parse_date(text)`: if `text` is exactly `YYYY-MM-DD` return `(year, month, day)` as ints, otherwise return `None`. `parse_date("2026-11-06")` is `(2026, 11, 6)`.

## Recap

- `re.findall`, `re.search`, `re.fullmatch` and `re.sub` find, test and replace patterns.
- Write patterns as raw strings; `\d`, `+`, `{n}`, `[ ]` and `( )` cover most needs.
- A failed `search` or `match` gives `None`: check before calling `.group()`.

## Common mistakes

- **Forgetting the `r` prefix**, so `"\d"` is treated as a broken escape.
- **Using `.group()` on `None`**: `AttributeError: 'NoneType' object has no attribute 'group'`.
- **Regex for everything.** If `split` or `startswith` does the job, use that: it is easier to read.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/05-text-and-files/06-regular-expressions
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

find_numbers: re.findall(r"\d+", text) returns every run of digits as text. Convert each one with int() to get a list of numbers.

</details>

<details><summary>Hint 2</summary>

find_hashtags: put parentheses around the part you want, r"#(\w+)", and findall returns just those groups: the word after each #.

</details>

<details><summary>Hint 3</summary>

parse_date: match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", text). If match is None return None, otherwise return tuple(int(part) for part in match.groups()).

</details>
