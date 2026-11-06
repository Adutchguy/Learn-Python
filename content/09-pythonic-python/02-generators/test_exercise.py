def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import inspect
import itertools

import pytest


def test_fibonacci_is_an_endless_generator():
    fibonacci = _fn("fibonacci")
    gen = fibonacci()
    assert inspect.isgenerator(gen), "fibonacci() should return a generator: use yield inside the function"
    first = list(itertools.islice(gen, 10))
    assert first == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], f"The first ten Fibonacci numbers are 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, got {first!r}"


def test_fibonacci_gives_a_fresh_sequence_each_call():
    fibonacci = _fn("fibonacci")
    a = fibonacci()
    next(a)
    next(a)
    assert next(fibonacci()) == 0, "each call to fibonacci() should start again from 0"


def test_chunks():
    chunks = _fn("chunks")
    assert list(chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]], f"chunks([1, 2, 3, 4, 5], 2) should be [[1, 2], [3, 4], [5]], got {list(chunks([1, 2, 3, 4, 5], 2))!r}"
    assert list(chunks([1, 2, 3], 3)) == [[1, 2, 3]], "a size equal to the length gives one chunk"
    assert list(chunks([], 4)) == [], "no items means no chunks"
    assert list(chunks("abcd", 3)) == ["abc", "d"], "slices of a string are strings, so chunks should keep the type of the slices"


def test_chunks_is_a_generator_and_validates_size():
    chunks = _fn("chunks")
    assert inspect.isgenerator(chunks([1], 1)), "chunks should be a generator function (use yield)"
    with pytest.raises(ValueError):
        list(chunks([1, 2], 0))


def test_running_total():
    running_total = _fn("running_total")
    assert list(running_total([1, 2, 3])) == [1, 3, 6], f"running_total([1, 2, 3]) should give 1, 3, 6, got {list(running_total([1, 2, 3]))!r}"
    assert list(running_total([])) == [], "no numbers means no totals"
    assert list(running_total([5, -5, 5])) == [5, 0, 5], "negative numbers should work too"


def test_running_total_is_lazy():
    running_total = _fn("running_total")
    pulled = []

    def source():
        for n in (1, 2, 3, 4):
            pulled.append(n)
            yield n

    gen = running_total(source())
    assert inspect.isgenerator(gen), "running_total should be a generator function (use yield)"
    assert pulled == [], "creating the generator must not read anything yet"
    assert next(gen) == 1, "the first total should be 1"
    assert pulled == [1], f"after one next() only one item should have been read, but {pulled!r} were read: yield each total as soon as you have it"
