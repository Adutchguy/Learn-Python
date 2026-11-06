# Booleans and Comparisons

*Foundations · about 15 minutes*

## Why this matters

Every decision a program makes comes down to a question with a yes/no answer: *is the password correct? is the cart empty? is it past noon?* In Python, yes/no values are called **booleans**, and you get them by comparing things.

## The idea

A **comparison** produces a `bool`, which is either `True` or `False`:

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | equal to | `3 == 3` | `True` |
| `!=` | not equal to | `3 != 4` | `True` |
| `<` `>` | less / greater than | `2 < 1` | `False` |
| `<=` `>=` | at most / at least | `5 >= 5` | `True` |

Careful: `==` **compares**; a single `=` **assigns**.

You can store the result like any other value:

```python
age = 15
is_teen = age >= 13 and age <= 19
print(is_teen)       # True
```

Combine booleans with `and`, `or` and `not`:

| Expression | Meaning | |
|---|---|---|
| `a and b` | both must be true | `True and False` → `False` |
| `a or b` | at least one must be true | `True or False` → `True` |
| `not a` | flips it | `not True` → `False` |

Python also lets you chain comparisons the way you would in maths: `13 <= age <= 19`.

Strings can be compared too: `"apple" == "apple"` is `True`, and capital letters matter: `"Apple" == "apple"` is `False`.

## Try it

Predict each result, then run it: `print(5 > 3)`, `print(5 == "5")`, `print(not (2 < 1))`, `print(10 % 2 == 0)`. The last one is a classic way to test whether a number is even.

## Your turn

A ride requires riders to be **at least 8 years old and at least 120 cm tall**. The starter reads an age and a height (in cm).

1. Create a variable `can_ride` that is `True` only when **both** requirements are met.
2. Print `can_ride`.

For an age of 10 and a height of 130 it prints `True`.

## Recap

- Comparisons (`==`, `!=`, `<`, `>`, `<=`, `>=`) give `True` or `False`.
- `and`, `or` and `not` combine or flip booleans.
- Compare with `==`; assign with `=`.

## Common mistakes

- **Using `=` instead of `==`** when comparing.
- **Quoting booleans:** `"True"` is text, not a boolean.
- **Mixing up `and` and `or`:** *at least 8 **and** at least 120 cm* needs both.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/01-foundations/09-booleans-and-comparisons
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

A comparison like age >= 8 already produces True or False. You can store it directly: old_enough = age >= 8

</details>

<details><summary>Hint 2</summary>

Combine two conditions with and: can_ride = age >= 8 and height >= 120

</details>

<details><summary>Hint 3</summary>

Then print the variable: print(can_ride)

</details>
