---
title: "Importing Modules"
minutes: 15
prereqs: ["06-errors-and-debugging/06-project-expense-tracker"]
concepts: ["import", "from import", "as", "math", "statistics", "standard library", "__name__", "main guard"]
local_only: false
hints:
  - "Put import math and import statistics at the top of the file. circle_area: return round(math.pi * radius ** 2, 2). pages_needed: math.ceil(items / per_page) rounds up."
  - "summarize: return {\"mean\": round(statistics.mean(numbers), 2), \"median\": statistics.median(numbers)}."
  - "main() just prints \"Area: \" followed by circle_area(2) (use print(\"Area:\", circle_area(2))). At the bottom, only call main() inside: if __name__ == \"__main__\": so that importing the file runs nothing."
---

## Why this matters

Python ships with a huge **standard library** of ready-made tools: maths, dates, files, JSON, random numbers and more. You use them with `import`. The same idea lets you split your own code across files.

## The idea

```python
import math                       # use as math.sqrt(16)
from math import sqrt, pi         # use as sqrt(16) and pi
import statistics as stats        # a shorter name: stats.mean([1, 2, 3])
```

`import math` is the safest: you always see where a name comes from. Avoid `from math import *`, which dumps every name into your file.

To learn what a module offers, use `help(math.ceil)` or `dir(math)`.

Every file has a built-in name, `__name__`. When you **run** the file it is `"__main__"`; when another file **imports** it, it is the module's name. That gives the standard pattern:

```python
def main():
    print("running")

if __name__ == "__main__":     # only when run directly, not when imported
    main()
```

## Try it

In the editor, `import math` and print `math.pi`, `math.sqrt(2)` and `math.floor(-2.5)`. Then add `print(__name__)` and see what it shows.

## Your turn

Write:

- `circle_area(radius)`: the area, rounded to 2 decimals (`circle_area(2)` is `12.57`). Use `math.pi`.
- `pages_needed(items, per_page)`: how many pages are needed to show `items` items with `per_page` on each page. 23 items at 10 per page need 3 pages. Use `math.ceil`.
- `summarize(numbers)`: a dictionary `{"mean": ..., "median": ...}` using the `statistics` module, with the mean rounded to 2 decimals.
- `main()` that prints `Area: 12.57` (using your `circle_area(2)`), called only under the `if __name__ == "__main__":` guard.

## Recap

- `import module` then `module.name`; `from module import name` for a few names.
- The standard library is big: look before you write your own.
- `if __name__ == "__main__":` runs code only when the file is run directly.

## Common mistakes

- **Naming your own file like a module** (`random.py`, `math.py`). Python imports yours instead and things break: `AttributeError: module 'random' has no attribute 'randint'`.
- **Forgetting the module name**: `sqrt(4)` after `import math` is a `NameError`.
- **Putting code at the top level of a file you want to import**, which then runs on import.
