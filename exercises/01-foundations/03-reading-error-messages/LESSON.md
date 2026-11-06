# Reading Error Messages

*Foundations · about 12 minutes*

## Why this matters

Everyone who writes code sees errors, constantly. Beginners panic; experienced programmers read them. An error message is Python telling you *exactly* what it could not do and *where*. Learning to read them is the single biggest time-saver you will pick up.

## The idea

When your program breaks, Python prints a **traceback**. Here is one:

```text
Traceback (most recent call last):
  File "exercise.py", line 3, in <module>
    print(nme)
NameError: name 'nme' is not defined
```

Read it **from the bottom up**:

1. **The last line** says what kind of error it is (`NameError`) and what went wrong (`name 'nme' is not defined`).
2. **The line above** shows the code that failed.
3. **`line 3`** tells you where to look.

The kinds you will meet most often early on:

| Error | What it means | Typical cause |
|---|---|---|
| `SyntaxError` | Python cannot understand how the code is written | a missing quote or bracket, a missing `:` |
| `NameError` | You used a name Python does not know | a typo in a variable name, or using it before creating it |
| `TypeError` | You used the wrong kind of value | adding text to a number |
| `ZeroDivisionError` | You divided by zero | `10 / 0` |
| `IndentationError` | The spacing at the start of a line is wrong | you will meet this with `if` soon |

Two habits to build: **fix one error at a time**, and **run again after every fix**. Fixing one problem often changes the next message.

## Try it

Make a mistake on purpose in the editor: type `print(hello)` without quotes, press Run, and read the last line. Then fix it and try a different mistake.

## Your turn

The program in the editor has **three bugs**. Each one produces a different error. Press **Run**, read the error, fix that bug, and repeat until the program prints exactly:

```text
Starting the program
Hello, Ada
Half of 10 is 5.0
```

## Recap

- Read a traceback from the bottom up: error type and message first, then the line number.
- `SyntaxError` means Python could not read the code; `NameError` means an unknown name.
- Fix one error at a time and run again.

## Common mistakes

- **Fixing the line Python points at when the real problem is the line before.** A missing `)` on one line often gets reported on the *next* line.
- **Changing many things at once.** You will not know which change helped.
- **Ignoring the message.** It is usually accurate. Read the actual words.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/01-foundations/03-reading-error-messages
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Press Run and read only the LAST line of the error. It names the kind of error and says what is wrong. Fix that one problem, then Run again.

</details>

<details><summary>Hint 2</summary>

Three bugs: a missing closing parenthesis on line 1, a misspelled variable name (nme) on line 3, and a division by zero on line 4.

</details>

<details><summary>Hint 3</summary>

Line 1 needs a ) at the end. Line 3 should use name. Line 4 should divide 10 by 2, not by 0.

</details>
