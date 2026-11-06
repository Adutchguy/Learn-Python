---
title: "Dictionaries: Looking Things Up by Name"
minutes: 18
prereqs: ["03-data-structures/05-tuples-and-unpacking"]
concepts: ["dictionary", "key", "value", "get", "items", "counting", "sorted keys"]
local_only: false
hints:
  - "Start with counts = {} and, for each word, update it: counts[word] = counts.get(word, 0) + 1. The 0 is the value used when the word is new."
  - "Make the text lower case first with .lower() so \"The\" and \"the\" count as the same word, then split it into words."
  - "To print in alphabetical order loop over sorted(counts): for word in sorted(counts): print(f\"{word}: {counts[word]}\"). Finish with the unique-word line using len(counts)."
---

## Why this matters

A list finds things by position. A **dictionary** finds them by *name*: a phone book that goes from a person to a number, a menu that goes from a dish to a price. It is one of the most useful tools in Python, and it is very fast, even with a million entries.

## The idea

```python
ages = {"Ada": 36, "Bo": 41}   # key: value pairs
print(ages["Ada"])             # 36
ages["Cy"] = 29                # add a new pair
ages["Bo"] = 42                # change an existing one
print("Bo" in ages)            # True   (checks the keys)
print(len(ages))               # 3

for name in ages:              # loops over the keys
    print(name, ages[name])
for name, age in ages.items(): # keys and values together
    print(name, age)
```

Asking for a key that is not there is a `KeyError`. `.get(key, default)` gives a fallback instead:

```python
print(ages.get("Zed", 0))      # 0
```

That unlocks the classic **counting** pattern:

```python
counts = {}
for letter in "banana":
    counts[letter] = counts.get(letter, 0) + 1
print(counts)                  # {'b': 1, 'a': 3, 'n': 2}
```

Keys must be unchangeable values like text, numbers or tuples. Dictionaries remember the order in which keys were added.

## Try it

Count the letters in your own name using the pattern above. Which letter appears most?

## Your turn

The starter reads a sentence. Count how many times each word appears, ignoring capital letters, and print the words in alphabetical order, then the number of different words:

```text
the: 2
cat: 1
```

For `The cat the` the output is:

```text
cat: 1
the: 2
Unique words: 2
```

## Recap

- `{key: value}` maps keys to values; read and write with `d[key]`.
- `.get(key, default)` avoids `KeyError`, which makes counting easy.
- Loop with `for key in d`, or `for key, value in d.items()`; use `sorted(d)` for alphabetical order.

## Common mistakes

- **`KeyError`** from reading a key that is missing. Use `.get()` or check with `in`.
- **Looking up by value.** Dictionaries are fast one way only: key to value.
- **Forgetting `.lower()`**, so "The" and "the" count separately.
