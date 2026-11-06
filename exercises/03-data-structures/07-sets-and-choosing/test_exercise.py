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


def test_overlapping_parties(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["ann bo cy", "bo cy di"],
        ["Both: bo, cy", "Only first: ann", "Only second: di", "Everyone: ann, bo, cy, di"],
    )


def test_nobody_in_common(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["ann bo", "cy di"],
        ["Both: nobody", "Only first: ann, bo", "Only second: cy, di", "Everyone: ann, bo, cy, di"],
    )


def test_same_guests_and_repeats(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["zed amy amy", "amy zed"],
        ["Both: amy, zed", "Only first: nobody", "Only second: nobody", "Everyone: amy, zed"],
    )
