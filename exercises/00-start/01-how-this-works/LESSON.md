# How This Works

*Start Here · about 5 minutes*

## Why this matters

You learn Python by *writing* it, not by reading about it. Every lesson here is a short read followed by hands-on practice. This five-minute tour shows you the tools, so nothing gets in your way later.

## The idea

Each lesson page has two halves: the lesson itself, and a **workspace** where you write code (under the lesson on a small screen). The workspace has:

- **The editor.** Type Python here. Your code is saved automatically in this browser, so you can close the page and come back.
- **Run ▶.** Runs your program and shows what it prints under **Output**. Running is free and safe, so do it as often as you like. Shortcut: Ctrl/⌘ + Enter.
- **Check ✔.** Runs the lesson's tests on your code and tells you, in plain language, what passed and what to fix.
- **Hints.** Three of them, each a little more revealing. Try to get as far as you can before opening the next one.
- **Show the solution.** Unlocks after a few unsuccessful checks. Looking is fine; just type it out yourself afterwards instead of copying.
- **Reset code.** Puts the starter code back if you want a fresh start.
- **Input box.** Some programs ask the person using them to type something. You type it here, before pressing Run.
- **Stop ■.** Appears while your program runs. If a program never finishes, press it.

## Try it

Press **Run** on the program in the editor. You should see two lines appear under Output. The program is only a few lines long: the first line prints a sentence, and the second prints a message with a number in it.

## Your turn

The program has a **variable** (a named piece of information) called `lucky_number`, currently set to `0`.

1. Change the `0` to `3`.
2. Press **Run** and look at the output.
3. Press **Check**.

## Recap

- **Run** shows what your program does; **Check** tests it against the lesson.
- Hints and the solution are there when you are stuck, not as a last resort.
- You cannot break anything. **Reset code** undoes it all.

## Common mistakes

- **Changing the code but not pressing Run or Check.** Nothing happens until you do.
- **Editing the comment instead of the code.** Lines that start with `#` are notes for humans; Python ignores them.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/00-start/01-how-this-works
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Find the line that says lucky_number = 0 in the editor.

</details>

<details><summary>Hint 2</summary>

Click inside the editor and replace the 0 with a 3.

</details>

<details><summary>Hint 3</summary>

The line should read exactly: lucky_number = 3

</details>
