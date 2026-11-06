def _run(monkeypatch, capsys, *typed):
    """Run the learner's program, typing `typed` one value at a time; return the module and its output."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError("Your program asked for more input than expected. Keep the two input() lines as they are.")

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise

    return exercise, capsys.readouterr().out.strip()


def _check(monkeypatch, capsys, age, height, expected):
    module, out = _run(monkeypatch, capsys, age, height)
    assert hasattr(module, "can_ride"), "Create a variable called can_ride: can_ride = ..."
    assert module.can_ride is expected, (
        f"For age {age} and height {height}, can_ride should be {expected}, but it is {module.can_ride!r}."
    )
    assert out == str(expected), (
        f"For age {age} and height {height}, your program should print {expected}, but it printed {out!r}."
    )


def test_old_and_tall_enough(monkeypatch, capsys):
    _check(monkeypatch, capsys, "10", "130", True)


def test_too_young(monkeypatch, capsys):
    _check(monkeypatch, capsys, "7", "130", False)


def test_too_short(monkeypatch, capsys):
    _check(monkeypatch, capsys, "10", "100", False)


def test_exactly_on_both_limits(monkeypatch, capsys):
    _check(monkeypatch, capsys, "8", "120", True)


def test_one_centimetre_short(monkeypatch, capsys):
    _check(monkeypatch, capsys, "30", "119", False)
