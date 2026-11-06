# Controlling Loops with break and continue

*Control Flow · about 15 minutes*

## Why this matters

Sometimes you do not know in advance when a loop should end (*keep asking until the user types "quit"*), or you want to skip certain items. `break` and `continue` give you precise control.

## The idea

- **`break`** ends the loop immediately.
- **`continue`** skips the rest of *this* pass and jumps to the next one.

```python
for number in range(1, 8):
    if number == 3:
        continue          # skip 3
    if number == 6:
        break             # stop completely at 6
    print(number)         # prints 1, 2, 4, 5
```

A very common pattern pairs `while True:` (a loop that never ends on its own) with `break` when a special **sentinel value** shows up:

```python
while True:
    word = input("Type a word (or 'quit'): ")
    if word == "quit":
        break
    print("You typed", word)
print("Goodbye")
```

This is often clearer than trying to squeeze the "stop" rule into the loop condition, especially when you need to read the input *before* you can decide.

Because `while True` never ends by itself, make sure there is always a path to `break`.

## Try it

Write a loop that prints the numbers 1 to 20, but skips multiples of 3 and stops completely when it reaches 15. (Hint: `number % 3 == 0` tests for a multiple of 3.)

## Your turn

Write a program that adds up numbers typed by the user:

- Keep asking with `input("Number: ")`.
- When the user types `0`, stop asking.
- **Negative numbers are ignored**: they are not added and not counted.
- At the end, print the sum, and how many numbers were added.

If the user types `5`, `3`, `0`, the output is:

```text
Sum: 8
Counted: 2
```

## Recap

- `break` leaves the loop; `continue` skips to the next pass.
- `while True:` plus `break` is the standard "keep going until I say stop" loop.
- A sentinel value (like `0` or `"quit"`) tells the program the input is finished.

## Common mistakes

- **Putting the sentinel check after using the value:** check for `0` first, before you add it.
- **Using `continue` before updating a counter** in a `while` loop. The condition never changes and the loop sticks.
- **No way out of `while True`.** If you forget the `break`, press **Stop ■**.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/02-control-flow/05-break-and-continue
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Use while True: to keep asking. Read the number with number = int(input("Number: ")) inside the loop.

</details>

<details><summary>Hint 2</summary>

If number == 0: break ends the loop. If number < 0: continue skips straight to the next question without counting it.

</details>

<details><summary>Hint 3</summary>

Otherwise add the number to total and add 1 to count. After the loop, print the two lines.

</details>
