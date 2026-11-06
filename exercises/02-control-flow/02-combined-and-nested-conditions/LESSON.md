# Combining and Nesting Conditions

*Control Flow · about 15 minutes*

## Why this matters

Real rules are rarely a single yes/no question: *free for children, but only on weekdays; members get a discount unless the item is already on sale.* You build rules like these by **combining** conditions and **nesting** `if` statements.

## The idea

You already know `and`, `or` and `not` from the Booleans lesson. They work directly inside `if`:

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("Come in")
```

`or` is true if either side is:

```python
day = "sat"
if day == "sat" or day == "sun":
    print("Weekend")
```

A shorter way to check against several options is the **`in`** operator:

```python
if day in ("sat", "sun"):
    print("Weekend")
```

You can also put an `if` **inside** another `if`. The inner one is indented further and only runs if the outer condition was true:

```python
if age >= 18:
    if has_ticket:
        print("Come in")
    else:
        print("Buy a ticket first")
else:
    print("Too young")
```

Nesting is great when a second question only makes sense after the first. When you can express the same thing with `and`, that is usually shorter and easier to read.

Another useful trick: a variable can be changed in one `if` and used in the next:

```python
price = 10
if day in ("sat", "sun"):
    price = price + 2
print(price)
```

## Try it

Rewrite the nested example above using `and` instead of nesting. Try different values of `age` and `has_ticket` and check you get the same results.

## Your turn

A cinema sets the ticket price from the customer's age:

| Age | Base price |
|---|---|
| under 5 | $0 (free) |
| 5 to 12 | $8 |
| 13 to 64 | $15 |
| 65 or over | $10 |

On **weekends** (`sat` or `sun`) every ticket that is not free costs **$2 more**. The starter reads the age and the day (always in lowercase, like `mon` or `sat`). Print the price in the form `Ticket: $17`.

## Recap

- Combine conditions in one `if` with `and`, `or` and `not`.
- `x in (a, b, c)` checks several options at once.
- Nest an `if` inside another when the second question depends on the first.

## Common mistakes

- **`if day == "sat" or "sun"`:** this does not do what it looks like. Write `day == "sat" or day == "sun"`, or use `in`.
- **Wrong indentation** in nested blocks: each level needs four more spaces.
- **Applying the surcharge to free tickets.** Check the price before adding.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/02-control-flow/02-combined-and-nested-conditions
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

First decide the base price from the age with if / elif / else. Ages under 5 are free, 5 to 12 cost 8, 13 to 64 cost 15, and 65 or over cost 10.

</details>

<details><summary>Hint 2</summary>

Then add the weekend surcharge: if day == "sat" or day == "sun" and the price is more than 0, add 2 to the price.

</details>

<details><summary>Hint 3</summary>

Print the result with print(f"Ticket: ${price}")

</details>
