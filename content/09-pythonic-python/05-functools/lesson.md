---
title: "functools: Caching, Partial Functions and Reduce"
minutes: 15
prereqs: ["09-pythonic-python/04-decorators"]
concepts: ["functools.cache", "functools.partial", "functools.reduce", "operator", "memoization"]
local_only: false
hints:
  - "Put @functools.cache on the line above def fib(n). The function body can stay the plain recursive version: if n < 2 return n, otherwise return fib(n - 1) + fib(n - 2). The decorator remembers answers so it stops being slow."
  - "square = functools.partial(power, exp=2) fixes the keyword argument exp. cube works the same with exp=3. Call them with just the base: square(5)."
  - "product: return functools.reduce(operator.mul, numbers, 1). The 1 at the end is the starting value, so an empty list gives 1."
---

## Why this matters

The standard library module `functools` is full of small tools that make functions more powerful. Three of them solve everyday problems: remembering answers, pre-filling arguments, and combining a list into one value.

## The idea

**`functools.cache`** is a decorator that remembers the result for each set of arguments. A slow recursive function becomes fast, because each answer is calculated only once:

```python
import functools

@functools.cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(80))             # instant; without @cache it would take years
print(fib.cache_info())    # hits, misses, size
```

This only suits functions whose result depends only on their arguments (no randomness, no printing, no changing outside data), and whose arguments are hashable.

**`functools.partial`** makes a new function with some arguments already filled in:

```python
def power(base, exp):
    return base ** exp

square = functools.partial(power, exp=2)
print(square(7))           # 49
```

**`functools.reduce`** squeezes a list down to one value by applying a two-argument function again and again. The `operator` module has the arithmetic operators as functions:

```python
import operator
functools.reduce(operator.add, [1, 2, 3, 4], 0)    # ((((0+1)+2)+3)+4) = 10
```

For plain sums, `sum()` is clearer. `reduce` shines when there is no built-in, such as a product.

## Try it

Run the examples. Call `fib.cache_info()` after `fib(10)` and after `fib(20)` and compare the `hits`.

## Your turn

The starter already has `power(base, exp)`. Add:

- `fib(n)`: the recursive Fibonacci (`fib(0)` is 0, `fib(1)` is 1) made fast with `functools.cache`.
- `square` and `cube`: made with `functools.partial` from `power`.
- `product(numbers)`: multiply all the numbers together with `functools.reduce`; the product of an empty list is `1`.

## Recap

- `@functools.cache` remembers results: great for pure functions with repeated calls.
- `functools.partial(f, ...)` pre-fills arguments and gives a new function.
- `functools.reduce(f, items, start)` folds items into one value.
- `operator.add`, `operator.mul` and friends are the operators as functions.

## Common mistakes

- **Caching functions with side effects**: the side effect only happens on a cache miss.
- **Forgetting the start value in `reduce`**, which makes an empty list raise `TypeError`.
- **Passing a list to a cached function**: lists are not hashable. Use a tuple.
