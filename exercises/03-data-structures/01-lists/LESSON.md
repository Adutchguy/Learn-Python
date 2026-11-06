# Lists: Keeping Many Values Together

*Data Structures · about 15 minutes*

## Why this matters

So far each variable has held one value. Real programs handle many: every name in a class, every price in a basket, every message in an inbox. A **list** holds many values in order, in one variable.

## The idea

```python
colors = ["red", "green", "blue"]
print(colors[0])        # red   (counting starts at 0)
print(colors[-1])       # blue  (-1 is the last item)
print(len(colors))      # 3

colors.append("pink")   # add to the end
colors.remove("green")  # remove the first "green"
print("red" in colors)  # True
print(colors)           # ['red', 'blue', 'pink']
```

Square brackets make a list, and `[0]`, `[1]`, ... pick items by **index** (position). `.append()` and `.remove()` change the list itself.

One more tool: `"milk eggs bread".split()` turns text into a list of words: `['milk', 'eggs', 'bread']`.

## Try it

Make a list of three of your favourite foods. Print the middle one using its index. Then try `print(colors[5])` on the list above. You will meet `IndexError: list index out of range`, which just means "there is no item at that position".

## Your turn

The starter reads a shopping list typed as words separated by spaces and turns it into a list called `items`. Leave those two lines alone. Then:

1. Add `"apples"` to the end of the list.
2. If `"eggs"` is in the list, remove it.
3. Print the first item, the last item and how many items are left, exactly like this:

```text
First: milk
Last: apples
Items: 3
```

## Recap

- A list is an ordered collection written with square brackets; items are found by index, starting at 0.
- `.append()` adds, `.remove()` deletes, `len()` counts, and `in` checks.
- `text.split()` makes a list of words from a string.

## Common mistakes

- **Counting from 1.** The first item is `[0]`, not `[1]`. Going too far gives `IndexError`.
- **Removing something that is not there** raises `ValueError`. Check with `in` first.
- **Expecting `append` to return the list.** It changes the list and returns nothing, so `items = items.append("x")` makes `items` equal to `None`.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/03-data-structures/01-lists
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

Add to a list with items.append(value). The new item goes on the end.

</details>

<details><summary>Hint 2</summary>

To remove "eggs" only when it is there, check first: if "eggs" in items: then items.remove("eggs"). Calling remove on a missing item is an error.

</details>

<details><summary>Hint 3</summary>

The first item is items[0] and the last is items[-1]. Print them with f-strings, and use len(items) for the count.

</details>
