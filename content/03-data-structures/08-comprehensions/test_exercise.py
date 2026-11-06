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


def test_example(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["1 2 3 4", "cat horse"],
        ["Even squares: [4, 16]", "Lengths: {'cat': 3, 'horse': 5}"],
    )


def test_no_even_numbers(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["3 5 7", "a"],
        ["Even squares: []", "Lengths: {'a': 1}"],
    )


def test_order_is_preserved(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["10 6 -2", "zebra ox"],
        ["Even squares: [100, 36, 4]", "Lengths: {'zebra': 5, 'ox': 2}"],
    )
