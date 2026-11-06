---
title: "itertools and random"
minutes: 18
prereqs: ["07-modules-and-tooling/03-dates-and-times"]
concepts: ["itertools", "combinations", "product", "chain", "random", "Random", "seed", "shuffle", "choice", "randint"]
local_only: false
hints:
  - "from itertools import combinations, product. all_pairs: return list(combinations(items, 2)). menu_combos: build the strings in a loop (or list comprehension) over product(mains, sides) and join each pair with \" + \"."
  - "roll_dice: [rng.randint(1, 6) for _ in range(count)]. Always call the methods on the rng you were given, not on the random module, or the results cannot be repeated."
  - "shuffled_copy: copy = list(items); rng.shuffle(copy); return copy. shuffle changes a list in place and returns None, so copy first. pick_winner: return rng.choice(names)."
---

## Why this matters

Two more useful corners of the standard library: `itertools` builds combinations without nested loops, and `random` adds chance to games, simulations and sampling. Both have a trick worth knowing.

## The idea

```python
from itertools import combinations, permutations, product, chain

list(combinations("abc", 2))      # [('a','b'), ('a','c'), ('b','c')]  order ignored
list(permutations("ab"))          # [('a','b'), ('b','a')]             order matters
list(product("ab", [1, 2]))       # [('a',1), ('a',2), ('b',1), ('b',2)]
list(chain([1, 2], [3]))          # [1, 2, 3]
```

These return **iterators** (lazy sequences), so wrap them in `list(...)` to see everything.

```python
import random

rng = random.Random(42)           # your own generator, with a seed
rng.randint(1, 6)                 # a whole number from 1 to 6, both included
rng.choice(["a", "b", "c"])       # one item
rng.shuffle(some_list)            # reorders the list IN PLACE
```

The same seed always gives the same sequence. That makes code that uses chance **testable**: take the generator as a parameter instead of calling `random` directly. For passwords and tokens use the `secrets` module instead; `random` is not secure.

## Try it

Print `list(combinations([1, 2, 3, 4], 3))`. Count the results, then use `permutations` and compare. Run `random.Random(1).randint(1, 6)` twice. Why is the answer the same?

## Your turn

Write five functions:

- `all_pairs(items)`: every pair of different items as a list of tuples, without repeats in a different order: `all_pairs(["a", "b", "c"])` is `[("a", "b"), ("a", "c"), ("b", "c")]`.
- `menu_combos(mains, sides)`: every main with every side as text like `"soup + bread"`, grouped by main.
- `roll_dice(count, rng)`: a list of `count` dice rolls (1 to 6) using the generator `rng`.
- `shuffled_copy(items, rng)`: a new shuffled list. The original must not change.
- `pick_winner(names, rng)`: one random name from the list.

## Recap

- `combinations`, `permutations` and `product` replace nested loops; wrap results in `list()`.
- A seeded `random.Random(seed)` repeats exactly; pass it in so your code can be tested.
- `shuffle` works in place and returns `None`.

## Common mistakes

- **`shuffled = random.shuffle(items)`**, which sets `shuffled` to `None`.
- **`randint(1, 6)` includes 6**, but `range(1, 6)` stops at 5.
- **Reading an iterator twice**: after one pass over `combinations(...)` it is empty.
