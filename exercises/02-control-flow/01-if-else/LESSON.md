# Making Decisions with if / elif / else

*Control Flow · about 15 minutes*

## Why this matters

Useful programs do different things in different situations: show an error when a password is wrong, give a discount to members, say "good morning" or "good evening". In Python, you make these choices with `if`.

## The idea

An `if` statement runs some code only when a condition is true:

```python
temperature = 30

if temperature > 20:
    print("Warm day")
```

Three details matter here:

1. The condition (`temperature > 20`) is followed by a **colon** `:`.
2. The code that belongs to the `if` is **indented** (four spaces is the convention). Indentation is how Python knows which lines are inside the `if`.
3. If the condition is false, the indented code is skipped.

Comparisons give you `True` or `False`: `>` greater than, `<` less than, `>=` greater than or equal, `<=` less than or equal, `==` equal to, `!=` not equal to. Note the **double** `==` for comparing; a single `=` is assignment.

Add `elif` ("else if") for more cases and `else` for everything left over. Python checks them top to bottom and runs only the **first** one that is true:

```python
score = 72

if score >= 90:
    print("A")
elif score >= 70:
    print("B")
else:
    print("Below B")
```

## Try it

Change `score` in the example above and run it a few times. Try 95, 70, 69 and 0. Can you predict the result before pressing Run?

## Your turn

The starter code asks the user for a temperature and stores it in `temperature`. (`input()` reads what the user types, and `int()` turns it into a number. You will learn how those work in a later lesson; for now, leave that line alone.)

Add an `if` / `elif` / `else` that prints exactly one word:

| Temperature | Print |
|---|---|
| 25 or higher | `Hot` |
| 15 or higher, but below 25 | `Nice` |
| anything lower | `Cold` |

In the **Input** box under the editor, type a number and press **Run** to try your program. **Check** will try several temperatures for you.

## Recap

- `if condition:` runs the indented block only when the condition is true.
- `elif` and `else` add more branches; only the first matching branch runs.
- Use `==` to compare and `=` to assign.

## Common mistakes

- **Forgetting the colon** after `if`, `elif` or `else` gives a `SyntaxError`.
- **Forgetting to indent** the block gives an `IndentationError`.
- **Using `=` instead of `==`** in a condition gives a `SyntaxError`.
- **Ordering conditions badly:** checking `>= 15` before `>= 25` would make 30 print `Nice`. Start with the most specific case.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/02-control-flow/01-if-else
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Start with the highest case: if temperature >= 25: and put print("Hot") on the next line, indented by four spaces.

</details>

<details><summary>Hint 2</summary>

Add a second check with elif temperature >= 15: that prints "Nice". Python only looks at the elif if the first condition was false.

</details>

<details><summary>Hint 3</summary>

Finish with else: and print("Cold"). The else needs no condition because it catches everything left over.

</details>
