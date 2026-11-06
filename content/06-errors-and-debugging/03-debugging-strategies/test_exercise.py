def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_average():
    average = _fn("average")
    assert average([2, 4, 6]) == 4, f"average([2, 4, 6]) should be 4 but was {average([2, 4, 6])!r}."
    assert average([10]) == 10, f"average([10]) should be 10 but was {average([10])!r}."


def test_count_vowels_lowercase():
    count_vowels = _fn("count_vowels")
    assert count_vowels("education") == 5, f"count_vowels('education') should be 5 but was {count_vowels('education')!r}."
    assert count_vowels("rhythm") == 0, "count_vowels('rhythm') should be 0."


def test_count_vowels_capitals():
    count_vowels = _fn("count_vowels")
    assert count_vowels("AEIOU") == 5, f"count_vowels('AEIOU') should be 5 but was {count_vowels('AEIOU')!r}. Capital letters count too."
    assert count_vowels("Education") == 5, f"count_vowels('Education') should be 5 but was {count_vowels('Education')!r}."


def test_last_n_normal_cases():
    last_n = _fn("last_n")
    assert last_n([1, 2, 3, 4], 2) == [3, 4], f"last_n([1, 2, 3, 4], 2) should be [3, 4] but was {last_n([1, 2, 3, 4], 2)!r}."
    assert last_n([1, 2], 5) == [1, 2], f"last_n([1, 2], 5) should be the whole list [1, 2] but was {last_n([1, 2], 5)!r}."


def test_last_n_zero_is_an_edge_case():
    last_n = _fn("last_n")
    assert last_n([1, 2, 3], 0) == [], f"last_n([1, 2, 3], 0) should be [] but was {last_n([1, 2, 3], 0)!r}. Remember that -0 is the same as 0."


def test_remove_negatives():
    remove_negatives = _fn("remove_negatives")
    result = remove_negatives([-1, -2, 3, -4, 5])
    assert result == [3, 5], f"remove_negatives([-1, -2, 3, -4, 5]) should be [3, 5] but was {result!r}. Check what happens when two negatives sit next to each other."
    assert remove_negatives([1, 2]) == [1, 2], "A list with no negatives should come back unchanged."
    assert remove_negatives([]) == [], "An empty list should give an empty list."
