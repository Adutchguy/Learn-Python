def _run(monkeypatch, capsys, *typed):
    """Run the learner's program, typing `typed` one value at a time; return what it printed."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError("Your program asked for more input than expected. Keep the two input() lines as they are.")

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise  # noqa: F401

    return capsys.readouterr().out.strip()


def _check(monkeypatch, capsys, age, day, price):
    out = _run(monkeypatch, capsys, age, day)
    expected = f"Ticket: ${price}"
    assert out == expected, (
        f"For age {age} on {day} your program should print {expected!r}, but it printed {out!r}."
    )


def test_toddler_on_a_weekday_is_free(monkeypatch, capsys):
    _check(monkeypatch, capsys, "3", "mon", 0)


def test_toddler_on_the_weekend_is_still_free(monkeypatch, capsys):
    _check(monkeypatch, capsys, "4", "sun", 0)


def test_child_on_a_weekday(monkeypatch, capsys):
    _check(monkeypatch, capsys, "10", "mon", 8)


def test_child_at_the_lower_boundary(monkeypatch, capsys):
    _check(monkeypatch, capsys, "5", "tue", 8)


def test_child_on_the_weekend(monkeypatch, capsys):
    _check(monkeypatch, capsys, "12", "sat", 10)


def test_adult_on_a_weekday(monkeypatch, capsys):
    _check(monkeypatch, capsys, "30", "fri", 15)


def test_adult_at_the_lower_boundary(monkeypatch, capsys):
    _check(monkeypatch, capsys, "13", "wed", 15)


def test_adult_on_the_weekend(monkeypatch, capsys):
    _check(monkeypatch, capsys, "30", "sun", 17)


def test_senior_on_a_weekday(monkeypatch, capsys):
    _check(monkeypatch, capsys, "70", "thu", 10)


def test_senior_at_the_boundary_on_the_weekend(monkeypatch, capsys):
    _check(monkeypatch, capsys, "65", "sat", 12)
