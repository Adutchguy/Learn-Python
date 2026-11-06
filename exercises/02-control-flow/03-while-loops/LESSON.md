# Repeating with while

*Control Flow · about 15 minutes*

## Why this matters

Computers are good at repeating things: checking every message, adding up every price, asking again until the answer is valid. A **loop** repeats a block of code. `while` repeats it for as long as a condition stays true.

## The idea

```python
count = 3
while count > 0:
    print(count)
    count = count - 1
print("Liftoff!")
```

This prints `3`, `2`, `1`, `Liftoff!`. Python follows these steps:

1. Check the condition (`count > 0`).
2. If it is true, run the indented block, then go back to step 1.
3. If it is false, skip the block and carry on below the loop.

Two patterns you will use constantly:

- A **counter** counts how many times something happened: `weeks = weeks + 1` (or the shorthand `weeks += 1`).
- An **accumulator** builds up a total: `total += price`.

Both need a **starting value** before the loop.

### The classic bug: the endless loop

If nothing inside the loop ever makes the condition false, it runs forever:

```python
count = 3
while count > 0:
    print(count)      # forgot to change count!
```

In this site, press **Stop ■** to stop a runaway program. Whenever you write a `while`, ask: *what changes each time round, and will that eventually make the condition false?*

## Try it

Write a `while` loop that doubles a number (starting at 1) until it is bigger than 1000, printing each value. How many values are printed?

## Your turn

You are saving for something that costs `goal` dollars by putting `deposit` dollars into a jar every week. The starter reads both numbers. Use a `while` loop to count the number of weeks until you have **at least** the goal, and print:

```text
Weeks needed: 4
```

(for a goal of 100 and a deposit of 30: after 4 weeks you have 120). If the goal is 0, you need 0 weeks.

## Recap

- `while condition:` repeats its block as long as the condition is true.
- Set up counters and accumulators *before* the loop and update them *inside* it.
- Make sure something in the loop moves towards ending it.

## Common mistakes

- **Forgetting to update the variable** the condition depends on, which causes an endless loop.
- **Initialising inside the loop**, which resets the counter every time.
- **Off-by-one errors:** `<` stops when equal; `<=` keeps going. Test the boundaries.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/02-control-flow/03-while-loops
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

You need two variables that start at 0: saved (money so far) and weeks (how many weeks have passed).

</details>

<details><summary>Hint 2</summary>

Loop with while saved < goal: and inside the loop add the deposit to saved and add 1 to weeks.

</details>

<details><summary>Hint 3</summary>

After the loop, print(f"Weeks needed: {weeks}")

</details>
