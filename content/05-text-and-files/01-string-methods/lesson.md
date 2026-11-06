---
title: "String Methods in Practice"
minutes: 15
prereqs: ["04-functions/08-project-quiz-engine"]
concepts: ["split", "join", "strip", "replace", "startswith", "isalpha", "isdigit", "string cleaning"]
local_only: false
hints:
  - "clean_name: split() with no argument splits on any run of spaces and drops the empties. Capitalise each piece and join them: \" \".join(word.capitalize() for word in raw.split()). A plain for loop that builds a list works too."
  - "initials: take the first letter of each word, upper-case it, and add a dot after it: \"A.L.\" for \"ada lovelace\"."
  - "is_palindrome: first build a string with only the letters of the text, in lower case (loop over the characters and keep those where ch.isalpha()). Then compare it with itself reversed: letters == letters[::-1]."
---

## Why this matters

Most real data is text: names typed by people, lines from files, web pages. It arrives messy, with extra spaces, odd capitals and punctuation. A handful of **string methods** clean most of it up.

## The idea

Strings cannot be changed, so every method returns a **new** string (or a list):

```python
raw = "  hello, Python World  "
raw.strip()                 # 'hello, Python World'    (trims both ends)
raw.lower(), raw.upper()
raw.title()                 # '  Hello, Python World  '
raw.replace("l", "L")       # swaps every 'l'
raw.split()                 # ['hello,', 'Python', 'World']  (on whitespace)
"a,b,c".split(",")          # ['a', 'b', 'c']               (on a separator)
"-".join(["a", "b"])        # 'a-b'
```

Asking questions about text:

```python
"python".startswith("py")   # True
"report.csv".endswith(".csv")   # True
"banana".count("a")         # 3
"banana".find("n")          # 2   (-1 if missing)
"abc".isalpha(), "123".isdigit(), "a1".isalnum()
```

Remember the pattern from lists: **split into pieces, work on each piece, join them back.**

## Try it

Take `"  the QUICK brown fox  "` and produce `"The Quick Brown Fox"` using `split`, `capitalize` and `join`.

## Your turn

Write three functions that **return** their answers:

- `clean_name(raw)`: tidy a typed name. Remove extra spaces and fix capitals: `clean_name("  aDA   LOVElace ")` is `"Ada Lovelace"`.
- `initials(name)`: `initials("ada lovelace")` is `"A.L."`.
- `is_palindrome(text)`: `True` if the text reads the same backwards, ignoring capitals, spaces and punctuation. `"A man, a plan, a canal: Panama"` is a palindrome.

## Recap

- String methods return new strings; the original never changes.
- `split` and `join` convert between text and lists; `strip` trims the ends.
- Test with `startswith`, `endswith`, `in`, `isalpha` and `isdigit`.

## Common mistakes

- **Expecting `text.strip()` to change `text`.** Assign the result: `text = text.strip()`.
- **`split(" ")` vs `split()`:** with an explicit space, repeated spaces produce empty strings.
- **Using `find` as a condition:** `-1` is truthy, and `0` (found at the start) is falsy.
