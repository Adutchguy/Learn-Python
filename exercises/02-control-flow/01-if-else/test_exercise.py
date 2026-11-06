def _run_with_input(monkeypatch, capsys, typed):
    """Run the learner's program as if the user had typed `typed`; return what it printed."""
    monkeypatch.setattr("builtins.input", lambda prompt="": typed)
    import exercise  # noqa: F401  (importing runs the learner's program)

    return capsys.readouterr().out.strip()


def _check(monkeypatch, capsys, typed, expected):
    out = _run_with_input(monkeypatch, capsys, typed)
    assert out == expected, (
        f"For a temperature of {typed}, your program should print {expected!r}, "
        f"but it printed {out!r}."
    )


def test_hot(monkeypatch, capsys):
    _check(monkeypatch, capsys, "30", "Hot")


def test_exactly_25_is_hot(monkeypatch, capsys):
    _check(monkeypatch, capsys, "25", "Hot")


def test_nice(monkeypatch, capsys):
    _check(monkeypatch, capsys, "20", "Nice")


def test_exactly_15_is_nice(monkeypatch, capsys):
    _check(monkeypatch, capsys, "15", "Nice")


def test_just_below_15_is_cold(monkeypatch, capsys):
    _check(monkeypatch, capsys, "14", "Cold")


def test_freezing_is_cold(monkeypatch, capsys):
    _check(monkeypatch, capsys, "-5", "Cold")
