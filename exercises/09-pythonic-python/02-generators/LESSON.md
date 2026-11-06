# Generators: Producing Values One at a Time

*Pythonic Python · about 18 minutes*

## Why this matters

Writing an iterator class works, but it is a lot of ceremony. A **generator** is a function that produces its values one at a time, and Python builds the iterator for you. Generators let you work with huge or even endless sequences using almost no memory.

## The idea

Put `yield` in a function and it becomes a generator function. Calling it does not run the body; it gives you a generator object. Each `next()` runs the body up to the next `yield`, hands that value out, and **pauses** right there:

```python
def count_up(limit):
    n = 1
    while n <= limit:
        yield n          # hand out n, then pause here
        n += 1           # resumes here on the next request

for n in count_up(3):
    print(n)             # 1, 2, 3
```

Because values are made on demand (**lazily**), a generator can describe an endless sequence:

```python
def naturals():
    n = 1
    while True:
        yield n
        n += 1
```

You must not call `list(naturals())`, which would never finish. Take a few with a loop and `break`, or with `itertools.islice(naturals(), 5)`.

A generator is an iterator, so it is used up after one pass, just like in the last lesson.

## Try it

Run `count_up`, then call `gen = count_up(2)` and `next(gen)` three times by hand. What happens on the third call?

## Your turn

Write three generator functions:

- `fibonacci()` yields `0, 1, 1, 2, 3, 5, ...` forever.
- `chunks(items, size)` yields lists of `size` items from `items`; the last one may be shorter. If `size` is less than 1, raise `ValueError`. (A generator raises when the first value is requested.)
- `running_total(numbers)` yields the running total: `[1, 2, 3]` gives `1, 3, 6`. It must be lazy: it may only read an item from `numbers` when asked for the next value.

## Recap

- `yield` makes a function a generator; each value is produced on demand.
- A generator pauses at `yield` and resumes where it left off.
- Generators can be endless, and they use very little memory.
- Use `itertools.islice` to take part of an endless generator.

## Common mistakes

- **Using `return` with a list** when the whole point is to avoid building one.
- **Calling `list()` on an endless generator**, which never finishes.
- **Reusing a used-up generator**: call the generator function again for a fresh one.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/09-pythonic-python/02-generators
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

A generator function uses yield instead of return. fibonacci: set a, b = 0, 1, then in an endless while True loop yield a and update with a, b = b, a + b.

</details>

<details><summary>Hint 2</summary>

chunks: raise ValueError("size must be at least 1") when size < 1, then loop for start in range(0, len(items), size) and yield items[start:start + size]. Slices past the end are just shorter, which handles the last chunk.

</details>

<details><summary>Hint 3</summary>

running_total: keep total = 0, then for number in numbers: total += number and yield total. Do NOT build a list first: yield each total as soon as you have it.

</details>
