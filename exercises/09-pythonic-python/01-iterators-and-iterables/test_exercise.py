def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _cls(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a class called {name}. Start it with: class {name}:"
    cls = getattr(exercise, name)
    assert isinstance(cls, type), f"{name} should be a class, but it is {cls!r}."
    return cls


import itertools


def test_countdown_counts_down():
    Countdown = _cls("Countdown")
    assert list(Countdown(3)) == [3, 2, 1], f"list(Countdown(3)) should be [3, 2, 1], got {list(Countdown(3))!r}"
    assert list(Countdown(1)) == [1], "Countdown(1) should give just [1]"
    assert list(Countdown(0)) == [], "Countdown(0) should give an empty list"


def test_countdown_works_in_a_for_loop_and_is_used_up():
    Countdown = _cls("Countdown")
    seen = []
    for number in Countdown(2):
        seen.append(number)
    assert seen == [2, 1], f"A for loop over Countdown(2) should see [2, 1], saw {seen!r}"
    counter = Countdown(2)
    list(counter)
    assert list(counter) == [], "An iterator is used up after one pass, so a second list() should be empty"


def test_countdown_is_its_own_iterator():
    Countdown = _cls("Countdown")
    counter = Countdown(2)
    assert iter(counter) is counter, "__iter__ should return self"
    assert next(counter) == 2, "the first next() should give the start value"


def test_first_n_basic():
    first_n = _fn("first_n")
    assert first_n([10, 20, 30, 40], 2) == [10, 20], f"first_n([10, 20, 30, 40], 2) should be [10, 20], got {first_n([10, 20, 30, 40], 2)!r}"
    assert first_n("abc", 3) == ["a", "b", "c"], "first_n should work on strings and give a list"
    assert first_n([1, 2], 5) == [1, 2], "with fewer items than n, return the items that exist"
    assert first_n([1, 2], 0) == [], "n of 0 should give an empty list"


def test_first_n_works_on_endless_iterables():
    first_n = _fn("first_n")
    result = first_n(itertools.count(5), 3)
    assert result == [5, 6, 7], f"first_n(itertools.count(5), 3) should be [5, 6, 7], got {result!r}"


def test_first_n_does_not_take_too_many():
    first_n = _fn("first_n")
    source = iter(range(10))
    assert first_n(source, 3) == [0, 1, 2], "the first three items should be 0, 1, 2"
    assert next(source) == 3, "first_n took more than n items from the iterator: the next unread item should be 3"
