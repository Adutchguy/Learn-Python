# Recursion: Functions That Call Themselves

*Functions · about 18 minutes*

## Why this matters

Some problems are naturally made of smaller copies of themselves: a folder containing folders, a sentence made of a word plus a shorter sentence. A **recursive** function solves such a problem by calling itself on a smaller piece. It is a powerful way of thinking, and you will meet it in file trees, parsers and many classic algorithms.

## The idea

Every recursive function needs two parts:

1. A **base case**: an answer so simple it needs no further calls. This stops the recursion.
2. A **recursive case**: solve a slightly smaller problem by calling yourself, then use that answer.

```python
def countdown(n):
    if n == 0:                # base case
        return ["Liftoff!"]
    return [n] + countdown(n - 1)   # recursive case

print(countdown(3))           # [3, 2, 1, 'Liftoff!']
```

Python keeps a stack of unfinished calls: `countdown(3)` waits for `countdown(2)`, which waits for `countdown(1)`, and so on. Each call must get closer to the base case. Without one you get `RecursionError: maximum recursion depth exceeded`.

Recursion is not always the best tool: a plain loop is often simpler and faster. Use it when the problem really is self-similar.

## Try it

Trace `countdown(2)` on paper: what does each call wait for, and what does it return? Then remove the base case and read the `RecursionError`.

## Your turn

Write three **recursive** functions (a loop is fine for your own experiments, but write these with recursion):

- `factorial(n)`: `factorial(5)` is `120` because `5 * 4 * 3 * 2 * 1`. Treat `factorial(0)` as `1`.
- `sum_digits(n)`: the sum of the digits of a whole number, so `sum_digits(493)` is `16`.
- `fibonacci(n)`: the Fibonacci sequence starts `0, 1, 1, 2, 3, 5, 8, 13`, where each number is the sum of the two before it. `fibonacci(0)` is `0`, `fibonacci(1)` is `1`, `fibonacci(7)` is `13`.

## Recap

- A recursive function has a base case that stops it and a recursive case that shrinks the problem.
- Each call waits on a smaller one; too deep means `RecursionError`.
- Prefer a loop when it is just as clear.

## Common mistakes

- **No base case, or one that is never reached**, so you get `RecursionError`.
- **Not shrinking the problem:** `factorial(n)` calling `factorial(n)` loops forever.
- **Very slow double recursion.** The Fibonacci version here repeats a lot of work; keep `n` small (about 25 or less).

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/04-functions/06-recursion
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

factorial: the base case is n <= 1, which returns 1. Otherwise return n * factorial(n - 1).

</details>

<details><summary>Hint 2</summary>

sum_digits: the base case is n < 10 (a single digit, return it). Otherwise the last digit is n % 10 and the rest is n // 10, so return n % 10 + sum_digits(n // 10).

</details>

<details><summary>Hint 3</summary>

fibonacci: there are two base cases. If n < 2, return n. Otherwise return fibonacci(n - 1) + fibonacci(n - 2).

</details>
