---
title: "Project: A Quiz Engine"
minutes: 35
prereqs: ["04-functions/07-docstrings-and-type-hints"]
concepts: ["project", "functions", "lists of tuples", "loops", "input", "string cleaning"]
local_only: false
hints:
  - "check_answer: compare cleaned-up text. given.strip().lower() == correct.strip().lower() is True when they match, ignoring spaces and capitals."
  - "run_quiz: keep score = 0. For each question, answer in the (question, correct) tuple, ask with input(question + \" \"), call check_answer, print Correct! or the Wrong! line, and add to score when right. Finally return score."
  - "grade: if score == total return \"Great job!\"; elif score * 2 >= total return \"Good effort!\"; otherwise return \"Keep practising!\". Use return, not print."
---

## Why this matters

Time to put functions, lists, tuples and loops together. You will finish a small **quiz engine**: it asks questions from a list, checks the answers forgivingly, and gives a score. The structure (data, small functions, a short main program) is how real programs are organised.

## The idea

The starter already has the data and the main program. Your job is to fill in three small functions, each doing one thing:

| Function | Job |
|---|---|
| `check_answer(given, correct)` | `True` if the answers match, ignoring spaces and capitals |
| `run_quiz(questions)` | ask every question, print feedback, **return** the score |
| `grade(score, total)` | **return** a message for the score |

Small functions are easier to test and to change. If you later want to read the questions from a file (a later module), only the data changes.

## Try it

Add a fourth question to the `QUESTIONS` list and run the program. Does everything still work? Think about why it does.

## Your turn

Complete the three functions. The main program at the bottom is already written: leave it alone.

**`run_quiz`** asks each question with `input(question + " ")`. After each answer print either `Correct!` or `Wrong! The answer was ANSWER` (using the stored answer). It returns the number of correct answers.

**`grade`** returns `Great job!` for a perfect score, `Good effort!` for half or more, and `Keep practising!` otherwise.

For answers `paris`, ` 4 ` and `green` the whole program prints:

```text
Correct!
Correct!
Wrong! The answer was blue
Score: 2/3
Good effort!
```

## Recap

- Break a program into small functions that each do one job and return their result.
- Keep data (the questions) separate from the code that uses it.
- A short main program that calls the functions reads like a summary.

## Common mistakes

- **Printing the score inside `run_quiz` instead of returning it.** The main program needs the number.
- **Comparing without cleaning**, so `"Paris "` or `"paris"` is wrongly marked wrong.
- **Changing the main program** to make a test pass instead of fixing the function.
