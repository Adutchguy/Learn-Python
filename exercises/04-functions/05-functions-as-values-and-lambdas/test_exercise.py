def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_apply_twice_with_a_lambda():
    result = _fn("apply_twice")(lambda n: n + 3, 10)
    assert result == 16, f"apply_twice(lambda n: n + 3, 10) should return 16 but returned {result!r}."


def test_apply_twice_with_a_builtin():
    result = _fn("apply_twice")(str.upper, "abc")
    assert result == "ABC", f"apply_twice(str.upper, 'abc') should return 'ABC' but returned {result!r}."


def test_apply_twice_really_calls_twice():
    seen = []

    def record(x):
        seen.append(x)
        return x + 1

    result = _fn("apply_twice")(record, 0)
    assert seen == [0, 1] and result == 2, f"func should be called twice, on 0 and then on 1. It was called with {seen!r} and the result was {result!r}."


def test_sort_people_oldest_first():
    people = [("Ada", 36), ("Bo", 41), ("Cy", 29)]
    result = _fn("sort_people")(people)
    assert result == [("Bo", 41), ("Ada", 36), ("Cy", 29)], f"sort_people should put the oldest first but returned {result!r}."


def test_sort_people_does_not_change_the_input():
    people = [("Ada", 36), ("Bo", 41)]
    _fn("sort_people")(people)
    assert people == [("Ada", 36), ("Bo", 41)], f"sort_people should not change the list it is given, but it is now {people!r}."


def test_longest_word():
    result = _fn("longest")(["pear", "fig", "banana"])
    assert result == "banana", f"longest(['pear', 'fig', 'banana']) should return 'banana' but returned {result!r}."


def test_longest_prefers_the_first_on_a_tie():
    result = _fn("longest")(["tree", "bush", "fig"])
    assert result == "tree", f"For a tie, longest should return the first word. longest(['tree', 'bush', 'fig']) should be 'tree' but was {result!r}."
