def _run(monkeypatch, capsys, *typed):
    """Run the learner's program, typing `typed` one value at a time; return what it printed."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError("Your program asked for more input than expected. Ask for the age only once.")

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise  # noqa: F401

    return capsys.readouterr().out.strip()


def _check(monkeypatch, capsys, age, expected):
    out = _run(monkeypatch, capsys, age)
    assert out == expected, (
        f"If the user types {age}, your program should print {expected!r}, but it printed {out!r}."
    )


def test_age_30(monkeypatch, capsys):
    _check(monkeypatch, capsys, "30", "Next year you will be 31")


def test_age_7(monkeypatch, capsys):
    _check(monkeypatch, capsys, "7", "Next year you will be 8")


def test_age_99(monkeypatch, capsys):
    _check(monkeypatch, capsys, "99", "Next year you will be 100")
