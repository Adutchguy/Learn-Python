# Project: Number Guessing Game

*Control Flow · about 30 minutes*

## Why this matters

You now know enough to build a real program. This project pulls together everything from the last two modules: input, conversion, comparisons, `if` / `elif` / `else`, `while`, counters and `break`.

## The idea

You are going to build the classic **number guessing game**. The program thinks of a secret number; the player keeps guessing, and the program says whether each guess is too low or too high.

Break the problem into small pieces and solve them one at a time. That is how professionals build things:

1. Ask for **one** guess and say whether it is too low, too high or right. (`if` / `elif` / `else`)
2. Make it **repeat** until the guess is right. (`while` and `break`)
3. **Count** the guesses. (a counter)
4. **Limit** the player to 7 guesses. (a loop condition, or a `break` rule)

Run your program after each step. A program that works at every step is much easier to fix than one you wrote all at once.

## Try it

Start with step 1 only: read a single guess and print `Too low!`, `Too high!` or `Correct!` Once that works, wrap it in a loop.

## Your turn

The starter has a `secret` number of 42. Write the game so that:

- Each round, it reads a guess with `int(input("Your guess: "))`.
- A guess below the secret prints `Too low!`; above prints `Too high!`.
- A correct guess prints `Correct! Guesses used: N` (where `N` is how many guesses the player made) and the game ends.
- The player gets **at most 7 guesses**. If all 7 are wrong, print `Out of guesses! The number was 42.` and the game ends.

For example, if the player types `50`, `25`, `42`, the output is:

```text
Too high!
Too low!
Correct! Guesses used: 3
```

**Going further (not checked):** replace `secret = 42` with a random number using `import random` and `secret = random.randint(1, 100)`. Then the game is different every time. Because the checks need a fixed secret, put it back to 42 before pressing **Check**.

## Recap

- Big programs are built by solving small steps one at a time.
- A counter plus a loop condition (or `break`) keeps loops under control.
- Reading the problem carefully ("at most 7", "ends the game") decides where the `break`s go.

## Common mistakes

- **Counting wrongly:** count a guess *every* time one is made, including the correct one.
- **Asking for an 8th guess:** the loop must stop after 7, even when they are all wrong.
- **Printing the "Out of guesses" line when the player won on guess 7.** Only print it if the player never got it right.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/02-control-flow/06-project-number-guessing-game
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Keep a counter, guesses = 0, and loop with while guesses < 7: so the game cannot go on forever.

</details>

<details><summary>Hint 2</summary>

Inside the loop: read the guess with int(input(...)), add 1 to guesses, then compare it with secret using if / elif / else. When the guess is right, print the success line and break.

</details>

<details><summary>Hint 3</summary>

After the loop, you need to know whether the player ever got it right. A True/False variable like found = False, which you set to True just before the break, does the job.

</details>
