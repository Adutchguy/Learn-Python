def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import pytest


def _run_main(monkeypatch, capsys, path, commands):
    import exercise

    capsys.readouterr()
    values = iter(commands)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError("The program asked for more input than the test typed.")

    monkeypatch.setattr("builtins.input", fake_input)
    exercise.main(str(path))
    return capsys.readouterr().out


def test_parse_expense_valid_lines():
    parse_expense = _fn("parse_expense")
    assert parse_expense("food 12.50") == ("food", 12.5), f"parse_expense('food 12.50') should return ('food', 12.5) but returned {parse_expense('food 12.50')!r}."
    assert parse_expense("  Coffee   3 ") == ("coffee", 3.0), f"parse_expense('  Coffee   3 ') should return ('coffee', 3.0) (lower-case category, float amount) but returned {parse_expense('  Coffee   3 ')!r}."


def test_parse_expense_wrong_number_of_parts():
    parse_expense = _fn("parse_expense")
    for line in ["", "food", "food 12.50 extra"]:
        with pytest.raises(ValueError) as info:
            parse_expense(line)
        assert str(info.value) == "expected CATEGORY AMOUNT, for example: food 12.50", f"parse_expense({line!r}) should raise ValueError('expected CATEGORY AMOUNT, for example: food 12.50') but the message was {str(info.value)!r}."


def test_parse_expense_amount_must_be_a_number():
    parse_expense = _fn("parse_expense")
    with pytest.raises(ValueError) as info:
        parse_expense("food lots")
    assert str(info.value) == "amount must be a number", f"parse_expense('food lots') should raise ValueError('amount must be a number') but the message was {str(info.value)!r}."


def test_parse_expense_amount_must_be_positive():
    parse_expense = _fn("parse_expense")
    for line in ["food 0", "food -4"]:
        with pytest.raises(ValueError) as info:
            parse_expense(line)
        assert str(info.value) == "amount must be positive", f"parse_expense({line!r}) should raise ValueError('amount must be positive') but the message was {str(info.value)!r}."


def test_save_and_load_round_trip(tmp_path):
    save_expense, load_expenses = _fn("save_expense"), _fn("load_expenses")
    path = tmp_path / "expenses.csv"
    save_expense(str(path), "food", 12.5)
    save_expense(str(path), "coffee", 3.0)
    assert path.read_text() == "food,12.5\ncoffee,3.0\n", f"The file should hold one 'category,amount' line per expense but holds {path.read_text()!r}. Open it in append mode so earlier lines are kept."
    assert load_expenses(str(path)) == [("food", 12.5), ("coffee", 3.0)], f"load_expenses should return [('food', 12.5), ('coffee', 3.0)] but returned {load_expenses(str(path))!r}."


def test_load_expenses_missing_file_is_not_an_error(tmp_path):
    load_expenses = _fn("load_expenses")
    result = load_expenses(str(tmp_path / "nope.csv"))
    assert result == [], f"A missing file means no expenses yet, so load_expenses should return [] but returned {result!r}."


def test_load_expenses_skips_bad_lines(tmp_path):
    load_expenses = _fn("load_expenses")
    path = tmp_path / "messy.csv"
    path.write_text("food,12.5\n\nbad line\nrent,abc\ncoffee,3\n")
    result = load_expenses(str(path))
    assert result == [("food", 12.5), ("coffee", 3.0)], f"Blank and broken lines should be skipped. Expected [('food', 12.5), ('coffee', 3.0)] but got {result!r}."


def test_totals_by_category():
    totals_by_category = _fn("totals_by_category")
    result = totals_by_category([("food", 10.0), ("rent", 500.0), ("food", 2.5)])
    assert result == {"food": 12.5, "rent": 500.0}, f"Expected {{'food': 12.5, 'rent': 500.0}} but got {result!r}."
    assert totals_by_category([("a", 0.1), ("a", 0.2)]) == {"a": 0.3}, "Round each total to 2 decimals, so 0.1 + 0.2 gives 0.3."
    assert totals_by_category([]) == {}, "No expenses should give an empty dictionary."


def test_format_report_empty():
    format_report = _fn("format_report")
    assert format_report({}) == "No expenses yet.", f"format_report({{}}) should return 'No expenses yet.' but returned {format_report({})!r}."


def test_format_report_layout_and_order():
    format_report = _fn("format_report")
    result = format_report({"food": 12.5, "rent": 500.0})
    expected = "rent        500.00\nfood         12.50\ntotal       512.50"
    assert result == expected, f"Expected:\n{expected}\n\nbut got:\n{result}\n(biggest amount first, category padded to 10, amount right-aligned in 8 with 2 decimals, then a total line)"


def test_format_report_ties_are_sorted_by_name():
    format_report = _fn("format_report")
    result = format_report({"b": 5.0, "a": 5.0})
    expected = "a             5.00\nb             5.00\ntotal        10.00"
    assert result == expected, f"Equal amounts should be listed alphabetically. Expected:\n{expected}\n\nbut got:\n{result}"


def test_main_session(monkeypatch, capsys, tmp_path):
    out = _run_main(monkeypatch, capsys, tmp_path / "e.csv", ["add food 12.5", "add Coffee 3", "add rent abc", "add 5", "add food -2", "bogus", "report", "quit"])
    expected = (
        "Expense tracker. Commands: add CATEGORY AMOUNT, report, quit\n"
        "Added 12.50 to food\n"
        "Added 3.00 to coffee\n"
        "Error: amount must be a number\n"
        "Error: expected CATEGORY AMOUNT, for example: food 12.50\n"
        "Error: amount must be positive\n"
        "Unknown command. Try: add food 12.50\n"
        "food         12.50\n"
        "coffee        3.00\n"
        "total        15.50\n"
    )
    assert out == expected, f"The session should print:\n{expected}\nbut printed:\n{out}"


def test_expenses_are_remembered_between_sessions(monkeypatch, capsys, tmp_path):
    path = tmp_path / "e.csv"
    _run_main(monkeypatch, capsys, path, ["add food 10", "quit"])
    out = _run_main(monkeypatch, capsys, path, ["add food 2.5", "report", "quit"])
    expected = "Expense tracker. Commands: add CATEGORY AMOUNT, report, quit\nAdded 2.50 to food\nfood         12.50\ntotal        12.50\n"
    assert out == expected, f"The second session should remember the first one. Expected:\n{expected}\nbut printed:\n{out}"
