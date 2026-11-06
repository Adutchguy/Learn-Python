# Repeating with for and range

*Control Flow · about 15 minutes*

## Why this matters

A `while` loop repeats *until a condition changes*. Very often, though, you know exactly how many times to repeat, or you want to do something for every item in a collection. That is what `for` is for, and it is the loop you will use most.

## The idea

```python
for letter in "abc":
    print(letter)
```

This prints `a`, `b`, `c`, one per line. On each pass, the **loop variable** (`letter`) holds the next value.

To repeat something a number of times, or to count, use `range()`:

```python
for i in range(3):
    print(i)           # 0, 1, 2
```

`range` can take up to three numbers:

| Call | Produces |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(2, 6)` | 2, 3, 4, 5 |
| `range(0, 10, 3)` | 0, 3, 6, 9 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

The **stop** value is never included. That surprises everyone once: `range(1, 4)` gives `1, 2, 3`. To include `n`, use `range(1, n + 1)`.

You can combine a `for` loop with an accumulator, exactly like with `while`:

```python
total = 0
for price in (5, 10, 20):
    total += price
print(total)           # 35
```

**When to use which loop:** use `for` when you know what you are looping over; use `while` when you are waiting for something to happen.

## Try it

Print the numbers from 10 down to 1 with a `for` loop, then print only the even numbers from 2 to 20.

## Your turn

The starter reads a number `n`. Write a `for` loop that

1. prints the **square** of every whole number from 1 up to and including `n`, one per line, and
2. after the loop, prints the total of those squares.

For `n = 5` the output is:

```text
1
4
9
16
25
Total: 55
```

## Recap

- `for item in something:` runs once for each item.
- `range(start, stop, step)` generates numbers; `stop` is excluded.
- Create accumulators before the loop and update them inside.

## Common mistakes

- **Forgetting that `range(n)` starts at 0** and stops *before* `n`.
- **Changing the loop variable inside the loop** and expecting it to affect the next pass. It will not.
- **Printing the total inside the loop** (you get a total on every line) instead of after it.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/02-control-flow/04-for-loops-and-range
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Set total = 0 before the loop. Then: for number in range(1, n + 1): gives you 1, 2, ... up to n.

</details>

<details><summary>Hint 2</summary>

Inside the loop, the square of a number is number * number (or number ** 2). Print it, and add it to total.

</details>

<details><summary>Hint 3</summary>

After the loop, print(f"Total: {total}")

</details>
