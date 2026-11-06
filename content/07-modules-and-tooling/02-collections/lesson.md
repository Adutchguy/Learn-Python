---
title: "The collections Module"
minutes: 18
prereqs: ["07-modules-and-tooling/01-importing-modules"]
concepts: ["collections", "Counter", "defaultdict", "deque", "namedtuple", "most_common"]
local_only: false
hints:
  - "top_words: from collections import Counter. counts = Counter(text.lower().split()), then return counts.most_common(n)."
  - "group_by_length: groups = defaultdict(list); loop over the words and call groups[len(word)].append(word); finish with return dict(groups)."
  - "rotate: from collections import deque; d = deque(items); d.rotate(k); return list(d). deque.rotate moves items to the right for positive k and to the left for negative k."
---

## Why this matters

Lists and dictionaries cover most needs, but a few patterns come up again and again: counting things, grouping things, and a queue you can add to at both ends. The `collections` module has a tool for each.

## The idea

```python
from collections import Counter, defaultdict, deque, namedtuple

Counter("banana")                     # Counter({'a': 3, 'n': 2, 'b': 1})
Counter("banana").most_common(1)      # [('a', 3)]

groups = defaultdict(list)            # a missing key starts as an empty list
groups["fruit"].append("apple")       # no KeyError, no setdefault needed

queue = deque([1, 2, 3])
queue.appendleft(0)                   # fast at both ends
queue.popleft()                       # take from the front
queue.rotate(1)                       # [3, 0, 1, 2] -> shifts items right

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p[1]                             # 3 4: named AND indexable, still a tuple
```

`Counter` ties are listed in the order the items were first seen.

## Try it

Count the letters of your name with `Counter`, then ask for the two most common ones. What happens when you look up a letter that is not there: `Counter("abc")["z"]`?

## Your turn

Write:

- `top_words(text, n)`: the `n` most common words as `(word, count)` tuples. Ignore capital letters and split on spaces. Use `Counter`.
- `group_by_length(words)`: a dictionary mapping a length to the list of words with that length, in their original order: `{1: ["a", "d"], 2: ["bb", "cc"]}`. Use `defaultdict(list)` and return an ordinary `dict`.
- `rotate(items, k)`: a new list with the items rotated `k` places to the right (`rotate([1, 2, 3, 4, 5], 2)` is `[4, 5, 1, 2, 3]`; a negative `k` rotates left). Use `deque.rotate`. The original list must not change.

## Recap

- `Counter` counts, `defaultdict` groups, `deque` is a double-ended queue.
- `namedtuple` gives tuple fields readable names.
- Import exactly what you need from `collections`.

## Common mistakes

- **Using a `defaultdict` and then reading a missing key by accident**, which silently creates it.
- **Calling `list.pop(0)` in a loop** on long lists; it is slow. A `deque` with `popleft()` is fast.
- **Forgetting that `Counter` returns 0 for missing items** instead of raising `KeyError`.
