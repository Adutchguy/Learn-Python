def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_circle_area():
    circle_area = _fn("circle_area")
    assert circle_area(2) == 12.57, f"circle_area(2) should be 12.57 but was {circle_area(2)!r}."
    assert circle_area(1) == 3.14, f"circle_area(1) should be 3.14 but was {circle_area(1)!r}."
    assert circle_area(0) == 0, "circle_area(0) should be 0."


def test_pages_needed_rounds_up():
    pages_needed = _fn("pages_needed")
    assert pages_needed(23, 10) == 3, f"pages_needed(23, 10) should be 3 but was {pages_needed(23, 10)!r}."
    assert pages_needed(20, 10) == 2, f"pages_needed(20, 10) should be 2 but was {pages_needed(20, 10)!r}."
    assert pages_needed(1, 10) == 1, "One item still needs one page."
    assert pages_needed(0, 10) == 0, "No items need no pages."


def test_pages_needed_returns_a_whole_number():
    pages_needed = _fn("pages_needed")
    assert isinstance(pages_needed(23, 10), int), f"pages_needed should return an int but returned {pages_needed(23, 10)!r}."


def test_summarize():
    summarize = _fn("summarize")
    assert summarize([1, 2, 3, 4, 10]) == {"mean": 4, "median": 3}, f"summarize([1, 2, 3, 4, 10]) should be {{'mean': 4, 'median': 3}} but was {summarize([1, 2, 3, 4, 10])!r}."
    assert summarize([1, 2, 3, 4]) == {"mean": 2.5, "median": 2.5}, f"summarize([1, 2, 3, 4]) should be {{'mean': 2.5, 'median': 2.5}} but was {summarize([1, 2, 3, 4])!r}."
    assert summarize([1, 2, 2])["mean"] == 1.67, f"The mean of [1, 2, 2] should be rounded to 1.67 but was {summarize([1, 2, 2])['mean']!r}."


def test_main_prints_the_area(capsys):
    import exercise

    capsys.readouterr()
    assert hasattr(exercise, "main"), "Define a function called main()."
    exercise.main()
    out = capsys.readouterr().out
    assert out == "Area: 12.57\n", f"main() should print 'Area: 12.57' but printed {out!r}."


def test_importing_the_file_prints_nothing(capsys):
    import exercise  # noqa: F401

    out = capsys.readouterr().out
    assert out == "", f"Importing your file should print nothing, but it printed {out!r}. Call main() only inside: if __name__ == \"__main__\":"
