---
title: Arithmetic and Operators
minutes: 15
prereqs: ["01-foundations/05-input-and-conversion"]
concepts: [operators, floor division, modulo, exponent, precedence]
local_only: false
hints:
  - "Whole hours: total_seconds // 3600. The leftover seconds after removing the hours: total_seconds % 3600."
  - "Take the leftover seconds and do the same with 60: minutes = leftover // 60, and seconds = leftover % 60."
  - "Finish with print(hours, \"h\", minutes, \"m\", seconds, \"s\")"
---

## Why this matters

Almost every program does some maths: totals, averages, conversions. Python has the usual operators plus two that are surprisingly useful: `//` and `%`.

## The idea

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` `-` | add, subtract | `7 - 2` | `5` |
| `*` | multiply | `3 * 4` | `12` |
| `/` | divide (always a `float`) | `7 / 2` | `3.5` |
| `//` | **floor** division: divide and drop the remainder | `7 // 2` | `3` |
| `%` | **modulo**: the remainder | `7 % 2` | `1` |
| `**` | power | `2 ** 3` | `8` |

`//` and `%` work as a pair: `7 // 2` is how many whole 2s fit into 7 (three), and `7 % 2` is what is left over (one).

**Order of operations** is like school maths: `**` first, then `*` `/` `//` `%`, then `+` `-`. Use brackets when in doubt: `(2 + 3) * 4` is `20`, but `2 + 3 * 4` is `14`.

A very common pattern is updating a variable using its own value:

```python
score = 10
score = score + 5   # 15
score += 5          # shorthand for the line above: 20
```

## Try it

Predict, then run: `print(17 // 5)`, `print(17 % 5)`, `print(2 ** 10)`, `print(2 + 3 * 4)`, `print((2 + 3) * 4)`.

## Your turn

The starter program reads a number of seconds. Convert it into hours, minutes and seconds with `//` and `%`, and print them like this (for `5000` seconds):

```text
1 h 23 m 20 s
```

Hint for thinking: there are 3600 seconds in an hour and 60 in a minute. Type a number in the **Input box** to try it; **Check** tries several.

## Recap

- `/` always gives a `float`; `//` gives whole-number division and `%` the remainder.
- `**` is power.
- Use brackets to make the order of operations obvious.

## Common mistakes

- **Expecting `7 / 2` to be `3`.** It is `3.5`. Use `//` for `3`.
- **Writing `^` for power.** In Python `^` is something else; use `**`.
- **Forgetting that input is text.** Convert with `int()` before calculating.
