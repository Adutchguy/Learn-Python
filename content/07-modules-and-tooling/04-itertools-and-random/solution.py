from itertools import combinations, product


def all_pairs(items):
    return list(combinations(items, 2))


def menu_combos(mains, sides):
    return [f"{main} + {side}" for main, side in product(mains, sides)]


def roll_dice(count, rng):
    return [rng.randint(1, 6) for _ in range(count)]


def shuffled_copy(items, rng):
    copy = list(items)
    rng.shuffle(copy)
    return copy


def pick_winner(names, rng):
    return rng.choice(names)
