---
title: "Testing with pytest: Writing Good Tests"
minutes: 20
prereqs: ["09-pythonic-python/04-decorators"]
concepts: ["pytest", "assert", "test functions", "edge cases", "pytest.raises", "mutation testing idea"]
local_only: false
hints:
  - "A test is a function whose name starts with test_ and that uses assert. Start with the plain case: assert slugify(\"Hello World\") == \"hello-world\". Give it a clear name like test_joins_words_with_hyphens."
  - "Think of the ways slugify could be wrong: capital letters (\"Hello\"), spaces at the start or end (\"  hi  \"), more than one space between words (\"a   b\"), and input that is not text. Write one small test for each."
  - "For the non-text case use pytest.raises: with pytest.raises(TypeError): slugify(42). The test passes only if that error happens. Your four tests then catch every broken version."
---

## Why this matters

Up to now the lessons tested your code for you. Real programmers write their own tests, because tests let you change code without fear: if you break something, a test tells you at once. **pytest** is the most popular tool for it, and you have been using it all along.

## The idea

A test is an ordinary function whose name starts with `test_`, containing one or more `assert` statements. If an `assert` fails, the test fails:

```python
def add(a, b):
    return a + b

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5
```

Run `pytest` in a terminal and it finds every `test_*` function in files named `test_*.py`, runs them, and prints a summary. A failure shows the line and both sides of the comparison.

Good tests:

- are **small**: one idea per test, with a name that says which idea;
- cover the **normal case** and the **edge cases**: empty input, one item, negative numbers, the biggest or smallest value;
- check **errors** with `pytest.raises`:

```python
import pytest

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

How do you know your tests are *good*? Ask: "would they notice if the function were broken?" Programmers sometimes check this by deliberately breaking the code (a **mutant**) and confirming that some test fails. A suite that passes on broken code is not protecting you.

## Try it

Run the example, then change `add` to `return a - b`. Which tests fail? Now try `return abs(a) + abs(b)`: do both still pass or not? What does that tell you about the first test?

## Your turn

The starter contains a working function `slugify(text)`: it lowercases the text, trims it, joins the words with single hyphens, and raises `TypeError` if `text` is not a string.

Write **at least four tests** for it, as functions starting with `test_` in the same file. The checks do two things:

1. Your tests must all pass on the correct `slugify`.
2. Your tests must **fail** on four deliberately broken versions: one that forgets to lowercase, one that mishandles spaces at the ends, one that mishandles several spaces in a row, and one that accepts non-text input.

## Recap

- A test is a `test_*` function with `assert`; pytest finds and runs them.
- Test the normal case, the edge cases and the errors (`pytest.raises`).
- Name each test after the behaviour it checks.
- Good tests fail when the code is broken.

## Common mistakes

- **Testing only the happy path.**
- **A test with no `assert`**, which can never fail.
- **One giant test** that checks ten things, so a failure does not tell you which.
