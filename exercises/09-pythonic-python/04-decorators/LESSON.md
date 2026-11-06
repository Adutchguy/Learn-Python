# Decorators: Wrapping Functions

*Pythonic Python · about 20 minutes*

## Why this matters

Sometimes you want to add behaviour to many functions (count calls, log them, retry on failure) without editing each one. A **decorator** wraps a function in another function. You will meet decorators everywhere: `@property`, `@dataclass`, web frameworks, test tools.

## The idea

Functions are values, so a function can take a function and return a new one:

```python
import functools

def shout(func):
    @functools.wraps(func)               # keep the original name and docstring
    def wrapper(*args, **kwargs):        # accept any arguments
        result = func(*args, **kwargs)   # call the real function
        return result.upper()            # change what comes out
    return wrapper

@shout
def greet(name):
    """Say hello."""
    return f"hello {name}"

print(greet("ada"))      # HELLO ADA
print(greet.__name__)    # greet   (thanks to functools.wraps)
```

`@shout` above `def greet` means exactly `greet = shout(greet)`.

A decorator that takes its own settings is a function that **returns a decorator**:

```python
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)            # repeat(3) runs first and gives back the real decorator
def hello():
    print("hi")
```

A function is an object, so a wrapper can keep state on itself, such as `wrapper.calls = 0`.

## Try it

Run the examples. Add `print("calling", func.__name__)` to `wrapper` in `shout` and see it appear.

## Your turn

1. `count_calls(func)`: a decorator that counts how often the function is called, in an attribute `calls` on the wrapper. Arguments and the return value pass through unchanged.
2. `retry(times)`: a decorator factory. The wrapped function is tried up to `times` times; if an attempt raises an exception, try again. If the last attempt fails too, let that exception escape. On success, return the result straight away.

Use `functools.wraps` in both so the function keeps its name and docstring.

## Recap

- A decorator is a function that takes a function and returns a function.
- `@deco` above `def f` means `f = deco(f)`.
- Use `*args, **kwargs` so the wrapper accepts any call, and `functools.wraps` to keep the identity.
- A decorator with settings is a function that returns a decorator.

## Common mistakes

- **Forgetting to `return` the wrapper** (the function becomes `None`).
- **Forgetting `return` inside the wrapper**, which throws the result away.
- **Calling the function instead of passing it**: `@retry` needs the number: `@retry(3)`.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/09-pythonic-python/04-decorators
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

count_calls(func) defines an inner wrapper(*args, **kwargs). Inside it do wrapper.calls += 1 and return func(*args, **kwargs). After the def, set wrapper.calls = 0 and return wrapper. Put @functools.wraps(func) on the line above def wrapper.

</details>

<details><summary>Hint 2</summary>

retry(times) is a function that returns a decorator. Structure: def retry(times): def decorator(func): @functools.wraps(func) def wrapper(*args, **kwargs): ... return wrapper; return decorator.

</details>

<details><summary>Hint 3</summary>

In retry's wrapper: for attempt in range(times): try: return func(*args, **kwargs) except Exception: if attempt == times - 1: raise. That re-raises the original error on the last attempt, and returns early on success.

</details>
