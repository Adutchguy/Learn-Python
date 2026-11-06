def _run(monkeypatch, capsys, *typed):
    """Run the learner's program, typing `typed` one value at a time; return what it printed."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError(
                "Your program asked for another number after the test had finished typing. "
                "Does your loop stop when the number is 0?"
            )

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise  # noqa: F401

    return capsys.readouterr().out


def _check(monkeypatch, capsys, typed, total, count):
    out = _run(monkeypatch, capsys, *typed)
    expected = f"Sum: {total}\nCounted: {count}\n"
    assert out == expected, (
        f"For the numbers {', '.join(typed)} your program should print:\n{expected}but it printed:\n{out}"
    )


def test_simple_sum(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["5", "3", "0"], 8, 2)


def test_negative_numbers_are_ignored(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["10", "-4", "6", "0"], 16, 2)


def test_zero_straight_away(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["0"], 0, 0)


def test_only_negative_numbers(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["-1", "-2", "0"], 0, 0)


def test_a_longer_list(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["1", "2", "3", "-9", "4", "0"], 10, 4)
