---
title: "Fixtures and Parametrize: Tests Without Repetition"
minutes: 20
prereqs: ["10-testing-and-quality/01-testing-with-pytest"]
concepts: ["fixtures", "@pytest.fixture", "parametrize", "test setup", "DRY tests"]
local_only: true
hints:
  - "A fixture is a function with @pytest.fixture above it that returns a ready-made object. Name it stack, create Stack(), call push for 1, 2 and 3, and return it."
  - "A test uses the fixture by adding a parameter with the same name: def test_peek_shows_the_top(stack): assert stack.peek() == 3. Write two or more tests like that (for example pop and len)."
  - "For parametrize: @pytest.mark.parametrize(\"value\", [1, \"a\", None, 3.5]) above def test_push_then_pop(value): create a Stack, push the value, and assert pop() returns it. pytest runs the test once per value."
---

## Why this matters

As test files grow, two kinds of repetition appear: the same setup code at the top of every test, and the same test copied with different numbers. pytest has a tool for each: **fixtures** and **parametrize**.

## The idea

A **fixture** is a function that prepares something your tests need. A test asks for it by naming it as a parameter, and pytest calls the fixture and passes the result in:

```python
import pytest

@pytest.fixture
def numbers():
    return [3, 1, 2]

def test_sorting(numbers):
    assert sorted(numbers) == [1, 2, 3]

def test_length(numbers):
    assert len(numbers) == 3
```

Every test gets its **own fresh** copy, so tests cannot affect each other. Fixtures can also create temporary files, open connections and clean up afterwards (with `yield`). pytest's built-in `tmp_path` and `capsys` are fixtures.

**`parametrize`** runs one test function with many inputs, and reports each as its own test:

```python
@pytest.mark.parametrize("text, expected", [
    ("a", 1),
    ("abc", 3),
    ("", 0),
])
def test_length_of_text(text, expected):
    assert len(text) == expected
```

The first argument names the parameters, the second is a list of value sets. A failure tells you exactly which set failed.

## Try it

This lesson uses real pytest features that the in-browser runner does not offer, so it runs on your own computer. Run the example in a file with `pytest -v` and look at the names in the output.

## Your turn

The starter has a working `Stack` class. Write the tests below it:

- A fixture called `stack` that returns a `Stack` with `1`, `2` and `3` pushed (in that order).
- At least **two** ordinary tests that use the `stack` fixture.
- A test decorated with `@pytest.mark.parametrize` and **at least three** sets of values.

The checker runs your file with pytest and counts the results.

## Recap

- `@pytest.fixture` prepares objects; tests receive them by parameter name.
- Each test gets a fresh fixture, so tests stay independent.
- `@pytest.mark.parametrize` turns one test into many.
- Both remove copy-paste from test files.

## Common mistakes

- **Calling the fixture like a function** (`stack()`) instead of asking for it as a parameter.
- **Sharing mutable state between tests** through a global variable.
- **Parametrize names that do not match** the test's parameter names.
