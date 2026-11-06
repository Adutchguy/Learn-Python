def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import random


def test_all_pairs():
    all_pairs = _fn("all_pairs")
    assert all_pairs(["a", "b", "c"]) == [("a", "b"), ("a", "c"), ("b", "c")], f"all_pairs(['a', 'b', 'c']) should be [('a', 'b'), ('a', 'c'), ('b', 'c')] but was {all_pairs(['a', 'b', 'c'])!r}."
    assert all_pairs([1]) == [], "One item makes no pairs."
    assert len(all_pairs(range(5))) == 10, "Five items make 10 different pairs."


def test_menu_combos():
    menu_combos = _fn("menu_combos")
    result = menu_combos(["soup", "salad"], ["bread", "rice"])
    assert result == ["soup + bread", "soup + rice", "salad + bread", "salad + rice"], f"Expected each main with each side, grouped by main, but got {result!r}."
    assert menu_combos(["soup"], []) == [], "No sides means no combinations."


def test_roll_dice_values_and_count():
    roll_dice = _fn("roll_dice")
    rolls = roll_dice(50, random.Random(1))
    assert len(rolls) == 50, f"roll_dice(50, rng) should return 50 rolls but returned {len(rolls)}."
    assert all(isinstance(r, int) and 1 <= r <= 6 for r in rolls), f"Every roll should be a whole number from 1 to 6 but got {rolls!r}."
    assert 6 in rolls and 1 in rolls, "With 50 rolls both 1 and 6 should appear. Use randint(1, 6): both ends are included."
    assert roll_dice(0, random.Random(1)) == [], "Zero rolls gives an empty list."


def test_roll_dice_uses_the_generator_it_is_given():
    roll_dice = _fn("roll_dice")
    first = roll_dice(10, random.Random(5))
    second = roll_dice(10, random.Random(5))
    assert first == second, "The same seed must give the same rolls. Call randint on the rng you were given, not on the random module."


def test_shuffled_copy_keeps_the_items():
    shuffled_copy = _fn("shuffled_copy")
    original = list(range(10))
    result = shuffled_copy(original, random.Random(3))
    assert sorted(result) == list(range(10)), f"The shuffled list must contain the same items, but it is {result!r}."
    assert result != list(range(10)), "A list of ten items should come back in a different order."
    assert original == list(range(10)), f"shuffled_copy must not change the original list, which is now {original!r}."
    assert result is not original, "Return a new list."


def test_shuffled_copy_is_repeatable():
    shuffled_copy = _fn("shuffled_copy")
    assert shuffled_copy(list(range(10)), random.Random(9)) == shuffled_copy(list(range(10)), random.Random(9)), "The same seed must give the same order. Shuffle with the rng you were given."


def test_pick_winner():
    pick_winner = _fn("pick_winner")
    names = ["Ada", "Bo", "Cy", "Di"]
    winner = pick_winner(names, random.Random(2))
    assert winner in names, f"The winner should be one of {names!r} but was {winner!r}."
    assert pick_winner(names, random.Random(4)) == pick_winner(names, random.Random(4)), "The same seed must pick the same name. Use rng.choice."
    assert pick_winner(["Solo"], random.Random(1)) == "Solo", "With one name that name must win."
    seen = {pick_winner(names, random.Random(seed)) for seed in range(40)}
    assert len(seen) > 1, "Different seeds should be able to pick different names."
