def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_clean_names_strips_and_title_cases():
    import pandas as pd

    df = pd.DataFrame({"name": ["  ada LOVELACE ", "bo", "CY  "], "age": [1, 2, 3]})
    result = _fn("clean_names")(df)
    assert result["name"].tolist() == ["Ada Lovelace", "Bo", "Cy"], (
        f"Names should be stripped and Title Case but are {result['name'].tolist()}."
    )
    assert result["age"].tolist() == [1, 2, 3], "The other columns should be left as they were."


def test_clean_names_does_not_change_the_original():
    import pandas as pd

    df = pd.DataFrame({"name": [" ada "]})
    _fn("clean_names")(df)
    assert df["name"].tolist() == [" ada "], "clean_names changed the table you passed in. Return a new table instead (for example with df.assign)."


def test_parse_prices_makes_numbers():
    import pandas as pd

    df = pd.DataFrame({"item": ["a", "b", "c"], "price": ["$1,200.50", "$35", "$0.99"]})
    result = _fn("parse_prices")(df)
    values = result["price"].tolist()
    assert values == [1200.5, 35.0, 0.99], f"The prices should be [1200.5, 35.0, 0.99] but are {values!r}."
    assert all(isinstance(v, float) for v in values), "The prices should be numbers (floats), not text."
    assert result["price"].sum() == 1236.49, "The converted column should add up like numbers."


def test_fill_missing_scores_uses_the_mean_of_known_scores():
    import numpy as np
    import pandas as pd

    df = pd.DataFrame({"name": ["a", "b", "c", "d"], "score": [90.0, np.nan, 70.0, np.nan]})
    result = _fn("fill_missing_scores")(df)
    assert result["score"].tolist() == [90.0, 80.0, 70.0, 80.0], (
        f"The missing scores should become the mean of the known ones (80.0) but the scores are {result['score'].tolist()}."
    )
    assert df["score"].isna().sum() == 2, "fill_missing_scores changed the table you passed in. Return a new table instead."


def test_unique_people_keeps_the_first_row():
    import pandas as pd

    df = pd.DataFrame({"name": ["Ada", "Bo", "Ada", "Cy", "Bo"], "visit": [1, 2, 3, 4, 5]})
    result = _fn("unique_people")(df)
    assert result["name"].tolist() == ["Ada", "Bo", "Cy"], f"Each name should appear once but the names are {result['name'].tolist()}."
    assert result["visit"].tolist() == [1, 2, 4], f"The first row for each name should be kept (visits 1, 2, 4) but the visits are {result['visit'].tolist()}."
    assert result.index.tolist() == [0, 1, 2], f"The row numbers should restart at 0 but are {result.index.tolist()}."
