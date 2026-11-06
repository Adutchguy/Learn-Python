---
title: Working with Text (Strings)
minutes: 15
prereqs: ["01-foundations/06-arithmetic"]
concepts: [string, concatenation, len(), indexing, string methods, strip, title]
local_only: false
hints:
  - "First clean the text: clean = name.strip().title(). strip() removes spaces at both ends and title() capitalises each word."
  - "Print the cleaned name with print(clean). Then print the number of characters with len(clean)."
  - "Finish with: print(\"Length:\", len(clean))"
---

## Why this matters

A huge share of real-world data is text: names, messages, addresses, web pages. Python makes working with text pleasant.

## The idea

You can combine and repeat strings:

```python
first = "Ada"
last = "Lovelace"
print(first + " " + last)   # Ada Lovelace   (+ joins text: "concatenation")
print("ha" * 3)             # hahaha
print(len("hello"))         # 5   (len() counts characters)
```

Each character has a position called an **index**, starting at **0**. Negative numbers count from the end:

```python
word = "python"
print(word[0])    # p
print(word[2])    # t
print(word[-1])   # n   (the last character)
```

Strings come with **methods**: actions you call with a dot after the value.

```python
text = "  Hello, World  "
print(text.strip())     # Hello, World   (removes spaces at both ends)
print(text.upper())     # "  HELLO, WORLD  "
print(text.lower())     # "  hello, world  "
print("ada lovelace".title())      # Ada Lovelace
print("a-b-c".replace("-", "+"))   # a+b+c
```

Methods do **not** change the original string; they give you a new one. To keep the result, store it: `text = text.strip()`. You can chain methods: `name.strip().title()`.

## Try it

Experiment: print `len("hello world")`, `"hello"[1]`, `"hello"[-2]`, and `"hello".upper()`. What happens with `"hello"[10]`? Read the error.

## Your turn

The starter program reads a name that might be messy: extra spaces, odd capital letters. Write a program that

1. cleans the name (no spaces at the ends, each word capitalised) and prints it, then
2. prints how many characters the cleaned name has.

For the input `  aDa LoVElace  ` it must print:

```text
Ada Lovelace
Length: 12
```

## Recap

- `+` joins strings, `*` repeats them, `len()` counts characters.
- Indexes start at 0; negative indexes count from the end.
- String methods like `strip()`, `upper()`, `lower()`, `title()` and `replace()` return new strings.

## Common mistakes

- **Mixing text and numbers with `+`:** `"Age: " + 30` is a `TypeError`. Convert with `str(30)` (the next lesson has a nicer way).
- **Starting to count at 1.** The first character is index 0.
- **Forgetting the brackets:** `name.strip` (no parentheses) does not call the method.
