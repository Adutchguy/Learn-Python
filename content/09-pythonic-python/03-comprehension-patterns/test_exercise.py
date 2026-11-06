def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _tracked(items):
    """An iterator that remembers how many items were taken from it."""
    taken = []

    def generate():
        for item in items:
            taken.append(item)
            yield item

    return generate(), taken


def test_flatten():
    flatten = _fn("flatten")
    assert flatten([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5], f"flatten([[1, 2], [3], [], [4, 5]]) should be [1, 2, 3, 4, 5], got {flatten([[1, 2], [3], [], [4, 5]])!r}"
    assert flatten([]) == [], "flatten of nothing should be an empty list"


def test_invert():
    invert = _fn("invert")
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}, f"invert({{'a': 1, 'b': 2}}) should be {{1: 'a', 2: 'b'}}, got {invert({'a': 1, 'b': 2})!r}"
    assert invert({}) == {}, "inverting an empty dict should give an empty dict"


def test_unique_lengths():
    unique_lengths = _fn("unique_lengths")
    result = unique_lengths(["hi", "yo", "hey", "wow", "there"])
    assert result == {2, 3, 5}, f"the distinct lengths should be {{2, 3, 5}}, got {result!r}"
    assert isinstance(result, set), "unique_lengths should return a set"


def test_label_parity():
    label_parity = _fn("label_parity")
    assert label_parity([1, 2, 3, 4]) == ["odd", "even", "odd", "even"], f"label_parity([1, 2, 3, 4]) should alternate odd/even, got {label_parity([1, 2, 3, 4])!r}"
    assert label_parity([]) == [], "no numbers means no labels"
    assert label_parity([0, -3]) == ["even", "odd"], "0 is even and -3 is odd"


def test_all_positive():
    all_positive = _fn("all_positive")
    assert all_positive([1, 2, 3]) is True, "all of 1, 2, 3 are positive"
    assert all_positive([1, 0, 3]) is False, "0 is not positive"
    assert all_positive([]) is True, "an empty list has no non-positive items, so the answer is True"


def test_all_positive_stops_early():
    all_positive = _fn("all_positive")
    source, taken = _tracked([5, -1, 7, 8])
    assert all_positive(source) is False, "a negative number is in the list"
    assert taken == [5, -1], f"all_positive should stop at the first non-positive number, but it read {taken!r}. Use a generator expression, not a list."


def test_any_long_and_early_stop():
    any_long = _fn("any_long")
    assert any_long(["hi", "elephant"], 5) is True, "'elephant' has at least 5 letters"
    assert any_long(["hi", "yo"], 3) is False, "no word has 3 letters"
    assert any_long([], 1) is False, "no words means False"
    source, taken = _tracked(["longword", "x", "y"])
    assert any_long(source, 4) is True, "'longword' is long enough"
    assert taken == ["longword"], f"any_long should stop at the first long word, but it read {taken!r}. Use a generator expression, not a list."
