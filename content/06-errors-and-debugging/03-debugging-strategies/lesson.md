---
title: "Debugging Strategies"
minutes: 20
prereqs: ["06-errors-and-debugging/02-raising-exceptions"]
concepts: ["debugging", "print debugging", "assert", "edge cases", "off-by-one", "mutating while looping", "reproduce"]
local_only: false
hints:
  - "average: the divisor should be exactly the number of items, len(numbers). Work out by hand what average([2, 4, 6]) should be, then compare."
  - "count_vowels fails on capital letters: lower-case the text first. last_n(items, 0) is a classic edge case: -0 is 0, so items[-0:] is the whole list. Handle n <= 0 separately."
  - "remove_negatives changes the list while looping over it, so the loop skips items. Do not remove inside the loop: build a new list instead, for example [n for n in numbers if n >= 0]."
---

## Why this matters

Programmers spend more time fixing code than writing it. The skill is not being lucky; it is a method. A good habit turns a mysterious failure into a short, boring search.

## The idea

1. **Reproduce it.** Find the smallest input that fails: `last_n([1, 2, 3], 0)`.
2. **Read the message.** The last line of a traceback names the error; the line above points at your code.
3. **Look at the values.** Print what is really there, not what you think is there. `f"{total=}"` prints both the name and the value:
   ```python
   total = 7
   print(f"{total=}")      # total=7
   ```
4. **Shrink the problem.** Cut code away (or add `print` calls halfway) until you know which half is wrong.
5. **Check your assumptions.** `assert len(items) > 0, "items is empty"` stops the program right where an assumption breaks.
6. **Explain it aloud** (the "rubber duck"). Saying what each line does often shows where it does not.

Most bugs are one of a handful of kinds: off-by-one, an edge case (empty, zero, one item, capitals), the wrong variable, or changing a list while looping over it.

## Try it

Predict what `last_n([1, 2, 3, 4], 2)` returns, then run it with a `print` inside. Then try `n = 0`.

## Your turn

The starter contains four functions. **Each one has a bug.** Fix all four without changing what they are supposed to do:

- `average(numbers)`: the mean of a list of numbers.
- `count_vowels(text)`: how many vowels (`a e i o u`, either case) are in the text.
- `last_n(items, n)`: the last `n` items as a new list (`[]` when `n` is 0 or less; the whole list if `n` is bigger than its length).
- `remove_negatives(numbers)`: a list without the negative numbers.

The test names and messages tell you what input failed. Reproduce, look, fix.

## Recap

- Reproduce with the smallest failing input, then look at real values.
- Use `print`/`f"{x=}"` and `assert` to check your assumptions.
- Suspect edge cases and lists being changed while you loop over them.

## Common mistakes

- **Changing several things at once.** Change one thing, run again.
- **Trusting the code instead of the output.** Print it.
- **Fixing the symptom** (special-casing one input) instead of the cause.
