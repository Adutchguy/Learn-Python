def _run(monkeypatch, capsys, *typed):
    """Run the learner's program, typing `typed` one value at a time; return what it printed."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError("Your program asked for more input than expected. Keep the input() lines as they are.")

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise  # noqa: F401

    return capsys.readouterr().out.strip()


def _check(monkeypatch, capsys, typed, expected):
    out = _run(monkeypatch, capsys, *typed)
    want = "\n".join(expected)
    assert out == want, (
        f"With the input {list(typed)!r} your program should print:\n{want}\n\nbut it printed:\n{out}"
    )


def test_seven_numbers(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["1 2 3 4 5 6 7"],
        ["First three: [1, 2, 3]", "Last two: [6, 7]", "Every other: [1, 3, 5, 7]", "Reversed: [7, 6, 5, 4, 3, 2, 1]"],
    )


def test_six_numbers(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["10 20 30 40 50 60"],
        ["First three: [10, 20, 30]", "Last two: [50, 60]", "Every other: [10, 30, 50]", "Reversed: [60, 50, 40, 30, 20, 10]"],
    )


def test_short_list(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["9 8"],
        ["First three: [9, 8]", "Last two: [9, 8]", "Every other: [9]", "Reversed: [8, 9]"],
    )
