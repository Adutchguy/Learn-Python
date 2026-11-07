def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _spending():
    import pandas as pd

    return pd.DataFrame(
        {
            "category": ["food", "travel", "food", "fun", "travel", "food"],
            "amount": [12.5, 40.0, 7.5, 20.0, 10.0, 5.0],
        }
    )


def test_total_by_category():
    result = _fn("total_by_category")(_spending())
    assert result == {"food": 25.0, "fun": 20.0, "travel": 50.0}, (
        f"The totals should be {{'food': 25.0, 'fun': 20.0, 'travel': 50.0}} but you returned {result!r}."
    )


def test_total_by_category_returns_a_plain_dict():
    result = _fn("total_by_category")(_spending())
    assert type(result) is dict, f"Return a plain dict (use .to_dict()), not {type(result).__name__}."


def test_average_by_rounds_to_two_places():
    import pandas as pd

    df = pd.DataFrame({"team": ["a", "a", "b", "b", "b"], "score": [1, 2, 1, 1, 2]})
    result = _fn("average_by")(df, "team", "score")
    assert result == {"a": 1.5, "b": 1.33}, f"The averages should be {{'a': 1.5, 'b': 1.33}} (rounded to 2 places) but you returned {result!r}."


def test_average_by_works_for_any_columns():
    result = _fn("average_by")(_spending(), "category", "amount")
    assert result == {"food": 8.33, "fun": 20.0, "travel": 25.0}, (
        f"Grouping the spending by category should give food 8.33, fun 20.0, travel 25.0 but you returned {result!r}."
    )


def test_busiest_category_counts_rows_not_amounts():
    result = _fn("busiest_category")(_spending())
    assert result == "food", (
        f"food appears in 3 rows (the most), but busiest_category returned {result!r}. "
        "Count the rows (value_counts), do not add up the amounts."
    )


def test_summary_table_columns_and_rows():
    import pandas as pd

    table = _fn("summary_table")(_spending())
    assert isinstance(table, pd.DataFrame), f"summary_table should return a DataFrame but returned {type(table).__name__}."
    assert list(table.columns) == ["category", "count", "mean"], (
        f"The columns should be ['category', 'count', 'mean'] but are {list(table.columns)}. "
        "Remember reset_index() so category is a normal column."
    )
    rows = table.to_dict("records")
    want = [
        {"category": "food", "count": 3, "mean": 8.33},
        {"category": "fun", "count": 1, "mean": 20.0},
        {"category": "travel", "count": 2, "mean": 25.0},
    ]
    assert rows == want, f"The rows should be {want} but are {rows}."
