def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


CSV = """date,product,units,price
2026-01-05,tea,10,2.50
2026-01-20,coffee,4,3.00
2026-02-03,tea,,2.50
2026-02-10,cake,6,4.25
2026-02-17,coffee,5,3.00
2026-03-01,tea,8,2.50
"""


def _sales():
    return _fn("load_sales")(CSV)


def test_load_sales_cleans_and_adds_revenue():
    import pandas as pd

    df = _sales()
    assert isinstance(df, pd.DataFrame), f"load_sales should return a DataFrame but returned {type(df).__name__}."
    assert list(df.columns) == ["date", "product", "units", "price", "revenue"], (
        f"The columns should be date, product, units, price, revenue but are {list(df.columns)}."
    )
    assert len(df) == 5, f"The row with no units should be dropped, leaving 5 rows, but there are {len(df)}."
    assert df.index.tolist() == [0, 1, 2, 3, 4], f"The row numbers should be 0 to 4 (use reset_index(drop=True)) but are {df.index.tolist()}."
    assert df["revenue"].tolist() == [25.0, 12.0, 25.5, 15.0, 20.0], f"revenue should be units * price but is {df['revenue'].tolist()}."


def test_load_sales_parses_dates():
    df = _sales()
    assert str(df["date"].dtype).startswith("datetime64"), (
        f"The date column should hold real dates (use pd.to_datetime) but has type {df['date'].dtype}."
    )


def test_revenue_by_month():
    result = _fn("revenue_by_month")(_sales())
    assert result == {"2026-01": 37.0, "2026-02": 40.5, "2026-03": 20.0}, (
        f"Monthly revenue should be {{'2026-01': 37.0, '2026-02': 40.5, '2026-03': 20.0}} but you returned {result!r}."
    )
    assert list(result) == ["2026-01", "2026-02", "2026-03"], "The months should be in order, earliest first."


def test_best_products_ranks_by_total_revenue():
    result = _fn("best_products")(_sales(), 2)
    assert result == [("tea", 45.0), ("coffee", 27.0)], f"The top 2 should be [('tea', 45.0), ('coffee', 27.0)] but you returned {result!r}."


def test_best_products_returns_everything_when_n_is_large():
    result = _fn("best_products")(_sales(), 10)
    assert [name for name, _ in result] == ["tea", "coffee", "cake"], (
        f"With n=10 all three products should come back, best first, but you returned {result!r}."
    )


def test_report_has_three_lines():
    text = _fn("report")(_sales())
    assert isinstance(text, str), f"report should return a string but returned {type(text).__name__}."
    want = "Total revenue: $97.50\nBest product: tea\nBusiest month: 2026-02"
    assert text.strip() == want, f"The report should be:\n{want}\n\nbut it was:\n{text}"
