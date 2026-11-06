# Looping Over Lists

*Data Structures · about 15 minutes*

## Why this matters

The point of a list is to do something with every item: add them up, find the biggest, show them to the user. A `for` loop does that, and it reads almost like English.

## The idea

```python
prices = [4, 9, 2]

for price in prices:
    print(price * 2)
```

`for price in prices:` runs the block once for each item, putting that item in `price`. No index, no `range`, no counter to mess up.

Python has shortcuts for common jobs:

```python
print(sum(prices))   # 15
print(max(prices))   # 9
print(min(prices))   # 2
```

When you need the position as well as the item, use `enumerate`:

```python
for position, price in enumerate(prices, start=1):
    print(f"{position}. {price}")   # 1. 4   2. 9   3. 2
```

## Try it

Write a loop that prints every item of `["a", "b", "c"]` in capitals. Then use `enumerate` to number them starting from 1.

## Your turn

The starter reads some whole numbers from one line into a list called `numbers` (leave those lines alone: they use a loop you already know). Print three lines:

```text
Total: 18
Largest: 8
Evens: 2
```

That is the sum, the biggest number, and how many of the numbers are even (for `5 3 8 2`: total 18, largest 8, evens 2).

## Recap

- `for item in list:` visits every item in order.
- `sum`, `max`, `min` and `len` summarise a list in one go.
- Use a counter or an accumulator when you need something the built-ins do not do, like counting evens.

## Common mistakes

- **Changing the list while looping over it**, such as removing items. Loop over a copy or build a new list instead.
- **Looping over `len(numbers)` by habit.** `for number in numbers:` is simpler and safer.
- **Resetting the counter inside the loop**, so it never grows.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/03-data-structures/02-looping-over-lists
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Start a counter before the loop (evens = 0), then inside the loop: if number % 2 == 0: evens += 1.

</details>

<details><summary>Hint 2</summary>

for number in numbers: gives you each item in turn. You can use sum(numbers) and max(numbers) for the first two lines.

</details>

<details><summary>Hint 3</summary>

Print each line with an f-string, for example print(f"Total: {sum(numbers)}"). The counter is only needed for the evens.

</details>
