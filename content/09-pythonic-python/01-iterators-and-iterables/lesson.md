---
title: "Iterators and Iterables: How for Loops Really Work"
minutes: 15
prereqs: ["08-oop/03-dunder-methods"]
concepts: ["iterable", "iterator", "iter()", "next()", "StopIteration", "__iter__", "__next__"]
local_only: false
hints:
  - "Countdown keeps the next number to hand out in self.current. __iter__ just returns self. __next__ raises StopIteration when self.current is 0 or less."
  - "In __next__: save value = self.current, then subtract 1 from self.current, then return value. Order matters: return the old value, not the new one."
  - "first_n: iterator = iter(iterable), then loop while len(items) < n: append next(iterator), and catch StopIteration with try/except to stop early. Checking the length BEFORE calling next means you never pull one item too many."
---

## Why this matters

Every `for` loop in Python uses one small protocol. Once you know it, you understand why lists, files, dictionaries and `range` all work in a `for` loop, and you can make your own classes loopable.

## The idea

An **iterable** is anything you can loop over (a list, a string, a file). An **iterator** is the object that hands out the items one at a time. `iter()` turns an iterable into an iterator, and `next()` asks for the next item:

```python
letters = iter("abc")
print(next(letters))   # a
print(next(letters))   # b
print(next(letters))   # c
print(next(letters))   # raises StopIteration: nothing left
```

A `for` loop is just a `while` loop that calls `next()` and quietly stops when it sees `StopIteration`. To make your own iterator, write a class with two methods:

```python
class Evens:
    def __init__(self, limit):
        self.n = 0
        self.limit = limit

    def __iter__(self):          # a loop asks for the iterator...
        return self              # ...and this object is its own iterator

    def __next__(self):          # ...then calls this again and again
        if self.n >= self.limit:
            raise StopIteration  # "I am finished"
        self.n += 2
        return self.n - 2

print(list(Evens(7)))            # [0, 2, 4, 6]
```

An iterator is **used up** after one pass. Looping over it a second time gives nothing.

## Try it

Run the example, then change `Evens(7)` to `Evens(0)`. What does `list()` give?

## Your turn

1. Write a class `Countdown(start)` that counts down to 1: `list(Countdown(3))` is `[3, 2, 1]`, and `list(Countdown(0))` is `[]`.
2. Write a function `first_n(iterable, n)` that returns a list of the first `n` items of any iterable. If there are fewer than `n` items, return what exists. It must work on **endless** iterables, and it must not take more than `n` items from the iterator.

## Recap

- An iterable can give you an iterator with `iter()`; `next()` returns the next item.
- `StopIteration` means "no more items". A `for` loop handles it for you.
- Your own iterator class needs `__iter__` (return `self`) and `__next__`.
- Iterators are used up after one pass.

## Common mistakes

- **Forgetting to raise `StopIteration`**, which makes the loop run forever.
- **Returning the updated value** instead of the one you just handed out.
- **Looping over the same iterator twice** and wondering why the second loop is empty.
