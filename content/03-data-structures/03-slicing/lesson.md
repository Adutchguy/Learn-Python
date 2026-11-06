---
title: "Slicing: Taking Part of a List"
minutes: 12
prereqs: ["03-data-structures/02-looping-over-lists"]
concepts: ["slice", "start:stop:step", "negative index", "reversing", "copy"]
local_only: false
hints:
  - "A slice looks like items[start:stop]. It includes start but stops before stop, so items[:3] is the first three items."
  - "For the last two use a negative start: items[-2:]. For every other item use a step: items[::2]."
  - "To reverse, use a step of -1: items[::-1]. Each result is a list, so print it directly."
---

## Why this matters

You often want a piece of a list: the first page of results, the last few messages, every other row. A **slice** does that in one short expression, and it works on strings too.

## The idea

```python
letters = ["a", "b", "c", "d", "e", "f"]
print(letters[1:4])    # ['b', 'c', 'd']   (index 1 up to, but not including, 4)
print(letters[:2])     # ['a', 'b']        (leave out the start: begin at 0)
print(letters[4:])     # ['e', 'f']        (leave out the stop: go to the end)
print(letters[-2:])    # ['e', 'f']        (the last two)
print(letters[::2])    # ['a', 'c', 'e']   (every second item)
print(letters[::-1])   # ['f', 'e', 'd', 'c', 'b', 'a']  (backwards)
```

The pattern is `[start:stop:step]`. The stop index is **not** included, so `letters[1:4]` has `4 - 1 = 3` items. A slice never causes an `IndexError`: if you ask for too much, you just get what exists.

The same works on text: `"python"[:2]` is `"py"`, and `"python"[::-1]` is `"nohtyp"`.

## Try it

Predict the result of `letters[2:5]`, `letters[:-1]` and `"hello"[1:3]`, then run them to check.

## Your turn

The starter reads whole numbers into a list called `numbers`. Use slices to print these four lines (the example is for `1 2 3 4 5 6 7`):

```text
First three: [1, 2, 3]
Last two: [6, 7]
Every other: [1, 3, 5, 7]
Reversed: [7, 6, 5, 4, 3, 2, 1]
```

The checks use lists of different lengths, so do not write the numbers out by hand.

## Recap

- `items[start:stop:step]` gives a new list; `stop` is excluded.
- Leave a part out to mean "from the beginning" or "to the end"; negative numbers count from the end.
- `[::-1]` reverses, and slices also work on strings.

## Common mistakes

- **Off-by-one with `stop`:** `items[0:3]` has three items (indexes 0, 1, 2), not four.
- **Confusing an index with a slice:** `items[-1]` is one item, while `items[-1:]` is a list holding that item.
- **Expecting a slice to change the original.** It makes a new list.
