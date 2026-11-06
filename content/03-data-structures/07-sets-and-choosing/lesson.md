---
title: "Sets, and Choosing the Right Structure"
minutes: 15
prereqs: ["03-data-structures/06-dictionaries"]
concepts: ["set", "union", "intersection", "difference", "duplicates", "choosing a structure"]
local_only: false
hints:
  - "Make each line a set: first = set(input().split()). Then first & second is the people in both, first - second is only the first group."
  - "Everyone is first | second. Sets have no order, so sort them before printing: sorted(group)."
  - "Turn each group into text with \", \".join(sorted(group)). If that is empty, use the word nobody: \", \".join(sorted(group)) or \"nobody\"."
---

## Why this matters

A **set** is a collection with no duplicates and no order. It is the right tool whenever you ask "is this in the group?" or "what do these two groups share?". Removing repeats from a list is one short line.

## The idea

```python
seen = {"a", "b", "a"}     # duplicates vanish: {'a', 'b'}
seen.add("c")
print("a" in seen)         # True, and very fast
print(set([1, 1, 2, 3, 3]))  # {1, 2, 3}
```

Careful: `{}` on its own is an empty *dictionary*. An empty set is `set()`.

Sets can be combined like Venn diagrams:

```python
a = {"ann", "bo", "cy"}
b = {"bo", "cy", "di"}
print(a & b)   # in both          {'bo', 'cy'}
print(a | b)   # in either        {'ann', 'bo', 'cy', 'di'}
print(a - b)   # only in a        {'ann'}
```

Because sets have no order, `print` may show items in any order. Sort when you need a predictable result: `sorted(a & b)`.

### Which structure should I use?

| You need... | Use |
|---|---|
| An ordered collection you will change, with repeats allowed | **list** |
| A fixed group of related values (a point, a record) | **tuple** |
| To look something up by a name or label | **dict** |
| Only uniqueness, or fast "is it in here?" and group maths | **set** |

## Try it

Remove the duplicates from `[3, 1, 3, 2, 1]` and print the result sorted.

## Your turn

Two lines are typed in: the guests at Alice's party, then the guests at Ben's party (names separated by spaces). Print who went to both, who went to only the first, who only the second, and everyone, each sorted alphabetically with `", "` between names. If nobody is in a group, print the word `nobody` instead.

```text
Both: bo, cy
Only first: ann
Only second: di
Everyone: ann, bo, cy, di
```

## Recap

- A set keeps unique items with no order; `set(list)` removes duplicates.
- `&` (both), `|` (either) and `-` (difference) combine sets.
- Pick the structure by the question you ask: order, grouping, lookup, or uniqueness.

## Common mistakes

- **`{}` is a dict, not a set.** Use `set()` for an empty one.
- **Expecting order** or indexing a set (`s[0]` is a `TypeError`).
- **Putting a list inside a set.** Items must be unchangeable: use a tuple.
