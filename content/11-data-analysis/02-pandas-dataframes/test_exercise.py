def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _frame():
    import pandas as pd

    return pd.DataFrame({"name": ["Ada", "Bo", "Cy"], "points": [30, 45, 38]})


def test_build_scores_makes_a_table():
    import pandas as pd

    df = _fn("build_scores")(["Ada", "Bo"], [30, 45])
    assert isinstance(df, pd.DataFrame), f"build_scores should return a pandas DataFrame but returned {type(df).__name__}."
    assert list(df.columns) == ["name", "points"], f"The columns should be ['name', 'points'] but are {list(df.columns)}."
    assert df["name"].tolist() == ["Ada", "Bo"], f"The name column should be ['Ada', 'Bo'] but is {df['name'].tolist()}."
    assert df["points"].tolist() == [30, 45], f"The points column should be [30, 45] but is {df['points'].tolist()}."


def test_top_scorer_is_the_name_with_most_points():
    result = _fn("top_scorer")(_frame())
    assert result == "Bo", f"Bo has the most points (45), but top_scorer returned {result!r}."


def test_top_scorer_when_the_best_is_first():
    import pandas as pd

    df = pd.DataFrame({"name": ["Zed", "Yan"], "points": [99, 3]})
    result = _fn("top_scorer")(df)
    assert result == "Zed", f"Zed has the most points, but top_scorer returned {result!r}."


def test_add_bonus_adds_a_total_column():
    df = _frame()
    result = _fn("add_bonus")(df, 5)
    assert "total" in result.columns, f"The result needs a 'total' column but has {list(result.columns)}."
    assert result["total"].tolist() == [35, 50, 43], f"total should be points + 5 = [35, 50, 43] but is {result['total'].tolist()}."


def test_add_bonus_leaves_the_original_alone():
    df = _frame()
    _fn("add_bonus")(df, 5)
    assert list(df.columns) == ["name", "points"], (
        f"add_bonus changed the table you passed in (its columns are now {list(df.columns)}). "
        "Return a new DataFrame instead, for example with df.assign(...)."
    )


def test_describe_points():
    result = _fn("describe_points")(_frame())
    assert isinstance(result, dict), f"describe_points should return a dict but returned {type(result).__name__}."
    assert set(result) == {"mean", "max", "min"}, f"The keys should be 'mean', 'max' and 'min' but are {sorted(result)}."
    assert abs(result["mean"] - 113 / 3) < 1e-9, f"The mean of 30, 45, 38 is 37.666... but you returned {result['mean']!r}."
    assert result["max"] == 45 and result["min"] == 30, f"max should be 45 and min 30 but you returned {result['max']!r} and {result['min']!r}."
    assert type(result["mean"]) is float and type(result["max"]) is float and type(result["min"]) is float, (
        "The values should be plain Python floats: wrap each in float(...)."
    )
