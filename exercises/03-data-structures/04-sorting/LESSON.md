# Sorting Lists

*Data Structures · about 15 minutes*

## Why this matters

Leaderboards, alphabetical contact lists, cheapest-first prices: sorting is everywhere. Python can sort almost anything with one call, and you control *how* with a **key**.

## The idea

```python
nums = [3, 1, 2]
print(sorted(nums))                # [1, 2, 3]   (a new list)
print(sorted(nums, reverse=True))  # [3, 2, 1]
nums.sort()                        # sorts nums itself and returns None
```

- `sorted(x)` returns a **new** sorted list and leaves `x` alone.
- `x.sort()` sorts `x` **in place** and returns nothing.

The `key` says what to sort by. It is a function that is applied to every item:

```python
words = ["pear", "Fig", "apple"]
print(sorted(words))                 # ['Fig', 'apple', 'pear']   capitals sort first!
print(sorted(words, key=str.lower))  # ['apple', 'Fig', 'pear']
print(sorted(words, key=len))        # ['Fig', 'pear', 'apple']
```

Python's sort is **stable**: items that tie keep their original order.

To print a list as text, join the items with a separator: `", ".join(["a", "b"])` is `"a, b"` (every item must be text).

## Try it

Sort `[10, 9, 100, 1]` as numbers, then sort `["10", "9", "100", "1"]` as text. Why are the answers different?

## Your turn

The starter reads names separated by spaces into a list called `names`. Print three lines, each with the names separated by a comma and a space (the example is for `bob alice Carol dave`):

```text
Sorted: alice, bob, Carol, dave
By length: bob, dave, alice, Carol
Reverse: dave, Carol, bob, alice
```

The first and last ignore capital letters. "By length" is shortest first.

## Recap

- `sorted()` returns a new list; `.sort()` changes the list and returns `None`.
- `key=` chooses what to sort by; `reverse=True` flips the order.
- `", ".join(items)` turns a list of strings into one string.

## Common mistakes

- **`names = names.sort()`** sets `names` to `None`. Use `sorted(...)` or call `.sort()` on its own line.
- **Forgetting capitals sort before lowercase** with the default sort.
- **Joining numbers.** `", ".join([1, 2])` is a `TypeError`: convert with `str()` first.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/03-data-structures/04-sorting
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

sorted(names, key=str.lower) sorts ignoring capital letters. Use ', '.join(...) to turn the sorted list into text.

</details>

<details><summary>Hint 2</summary>

To sort by length use key=len. Equal lengths stay in their original order, so you do not need a second rule.

</details>

<details><summary>Hint 3</summary>

For the reverse line add reverse=True to the case-insensitive sort: sorted(names, key=str.lower, reverse=True).

</details>
