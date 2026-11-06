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


def _check(monkeypatch, capsys, goal, deposit, weeks):
    out = _run(monkeypatch, capsys, goal, deposit)
    expected = f"Weeks needed: {weeks}"
    assert out == expected, (
        f"For a goal of {goal} and {deposit} a week your program should print {expected!r}, "
        f"but it printed {out!r}."
    )


def test_goal_not_hit_exactly(monkeypatch, capsys):
    _check(monkeypatch, capsys, "100", "30", 4)


def test_goal_hit_exactly(monkeypatch, capsys):
    _check(monkeypatch, capsys, "90", "30", 3)


def test_two_weeks(monkeypatch, capsys):
    _check(monkeypatch, capsys, "100", "50", 2)


def test_one_deposit_is_enough(monkeypatch, capsys):
    _check(monkeypatch, capsys, "10", "100", 1)


def test_goal_of_zero_needs_no_weeks(monkeypatch, capsys):
    _check(monkeypatch, capsys, "0", "5", 0)
