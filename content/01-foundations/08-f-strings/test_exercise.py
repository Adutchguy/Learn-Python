def _run(monkeypatch, capsys, *typed):
    """Run the learner's program, typing `typed` one value at a time; return what it printed."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError("Your program asked for more input than expected. Keep the three input() lines as they are.")

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise  # noqa: F401

    return capsys.readouterr().out.strip()


def _check(monkeypatch, capsys, item, price, quantity, expected):
    out = _run(monkeypatch, capsys, item, price, quantity)
    assert out == expected, (
        f"For {item!r}, {price} and {quantity} your program should print {expected!r}, "
        f"but it printed {out!r}."
    )


def test_coffee(monkeypatch, capsys):
    _check(monkeypatch, capsys, "Coffee", "2.5", "3", "3 x Coffee at $2.50 = $7.50")


def test_tea(monkeypatch, capsys):
    _check(monkeypatch, capsys, "Tea", "1.99", "2", "2 x Tea at $1.99 = $3.98")


def test_whole_dollar_price(monkeypatch, capsys):
    _check(monkeypatch, capsys, "Cake", "4", "1", "1 x Cake at $4.00 = $4.00")
