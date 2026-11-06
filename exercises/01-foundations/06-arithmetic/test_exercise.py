def _run(monkeypatch, capsys, typed):
    """Run the learner's program as if the user had typed `typed`; return what it printed."""
    monkeypatch.setattr("builtins.input", lambda prompt="": typed)
    import exercise  # noqa: F401

    return capsys.readouterr().out.strip()


def _check(monkeypatch, capsys, seconds, expected):
    out = _run(monkeypatch, capsys, seconds)
    assert out == expected, (
        f"For {seconds} seconds your program should print {expected!r}, but it printed {out!r}."
    )


def test_5000_seconds(monkeypatch, capsys):
    _check(monkeypatch, capsys, "5000", "1 h 23 m 20 s")


def test_under_a_minute(monkeypatch, capsys):
    _check(monkeypatch, capsys, "59", "0 h 0 m 59 s")


def test_exactly_one_hour(monkeypatch, capsys):
    _check(monkeypatch, capsys, "3600", "1 h 0 m 0 s")


def test_just_under_a_day(monkeypatch, capsys):
    _check(monkeypatch, capsys, "86399", "23 h 59 m 59 s")
