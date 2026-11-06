---
title: "f-strings: Building Text from Values"
minutes: 12
prereqs: ["01-foundations/07-strings"]
concepts: [f-string, string formatting, format specifier]
local_only: false
hints:
  - "Start the string with f before the opening quote, and put expressions inside curly braces: f\"{quantity} x {item}\""
  - "Format a number with two decimals by adding :.2f inside the braces, like {price:.2f}. The total is price * quantity."
  - "print(f\"{quantity} x {item} at ${price:.2f} = ${price * quantity:.2f}\")"
---

## Why this matters

Programs constantly build sentences out of values: receipts, messages, reports. Gluing text together with `+` and `str()` gets messy fast. **f-strings** are the modern, readable way.

## The idea

Put an `f` in front of the opening quote, and write any variable or calculation inside `{ }`:

```python
name = "Ada"
age = 36
print(f"{name} is {age} years old")        # Ada is 36 years old
print(f"Next year: {age + 1}")              # Next year: 37
```

Everything in the braces is evaluated, so you do not need `str()`.

You can also control how a value is shown by adding a **format specifier** after a colon:

```python
price = 2.5
print(f"{price:.2f}")        # 2.50   (exactly 2 decimal places)
print(f"{1234567:,}")        # 1,234,567   (thousands separators)
print(f"{0.256:.0%}")        # 26%   (as a percentage)
```

`.2f` is the one you will use most: "a float with 2 digits after the point". Handy for money. A literal dollar sign needs no special treatment: `f"${price:.2f}"` prints `$2.50`.

## Try it

Make a few f-strings of your own: print a sentence with your name and a calculation inside it, and format a number with `:.1f`, `:.2f` and `:,`.

## Your turn

The starter reads an item name, a price per item and a quantity. Print one receipt line. For `Coffee`, `2.5` and `3` it must print exactly:

```text
3 x Coffee at $2.50 = $7.50
```

Use a single f-string. Type the three inputs (one per line) in the **Input box** to try it.

## Recap

- `f"text {value}"` puts values straight into text.
- Anything can go inside the braces, including calculations.
- `{x:.2f}` shows a float with two decimals.

## Common mistakes

- **Forgetting the `f`:** without it, Python prints the braces literally.
- **Quotes inside the braces:** if your f-string uses double quotes, use single quotes for anything inside it (and vice versa).
- **Rounding when you meant to format:** `:.2f` only changes how the number is *shown*, which is what you want for display.
