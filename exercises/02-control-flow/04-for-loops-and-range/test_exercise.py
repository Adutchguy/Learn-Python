def _run(monkeypatch, capsys, typed):
    """Run the learner's program as if the user had typed `typed`; return what it printed."""
    monkeypatch.setattr("builtins.input", lambda prompt="": typed)
    import exercise  # noqa: F401

    return capsys.readouterr().out


def _check(monkeypatch, capsys, n, expected_lines):
    out = _run(monkeypatch, capsys, n)
    expected = "\n".join(expected_lines) + "\n"
    assert out == expected, (
        f"For n = {n} your program should print:\n{expected}but it printed:\n{out}"
    )


def test_five_squares(monkeypatch, capsys):
    _check(monkeypatch, capsys, "5", ["1", "4", "9", "16", "25", "Total: 55"])


def test_just_one(monkeypatch, capsys):
    _check(monkeypatch, capsys, "1", ["1", "Total: 1"])


def test_zero_prints_only_the_total(monkeypatch, capsys):
    _check(monkeypatch, capsys, "0", ["Total: 0"])


def test_ten_squares_include_n_itself(monkeypatch, capsys):
    squares = [str(i * i) for i in range(1, 11)]
    _check(monkeypatch, capsys, "10", squares + ["Total: 385"])
