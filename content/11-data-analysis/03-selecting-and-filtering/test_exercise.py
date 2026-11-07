def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _people():
    import pandas as pd

    return pd.DataFrame(
        {
            "name": ["Ada", "Bo", "Cy", "Di", "Ed"],
            "age": [34, 17, 45, 29, 18],
            "city": ["Rome", "Oslo", "Rome", "Oslo", "Lima"],
        }
    )


def test_adults_keeps_only_18_and_over():
    result = _fn("adults")(_people())
    assert result["name"].tolist() == ["Ada", "Cy", "Di", "Ed"], (
        f"adults should keep ages 18 or more (Ada, Cy, Di, Ed) but kept {result['name'].tolist()}. "
        "Ed is exactly 18, which counts as an adult."
    )


def test_names_in_city_combines_two_conditions():
    result = _fn("names_in_city")(_people(), "Rome")
    assert result == ["Ada", "Cy"], f"The adults in Rome are Ada and Cy but names_in_city returned {result!r}."
    result = _fn("names_in_city")(_people(), "Oslo")
    assert result == ["Di"], f"Bo is in Oslo but is only 17, so only Di should be returned; you returned {result!r}."


def test_names_in_city_is_a_plain_list():
    result = _fn("names_in_city")(_people(), "Lima")
    assert isinstance(result, list), f"Return a plain list (use .tolist()), not {type(result).__name__}."
    assert result == ["Ed"], f"The only adult in Lima is Ed but you returned {result!r}."


def test_select_columns():
    result = _fn("select_columns")(_people(), ["name", "city"])
    assert list(result.columns) == ["name", "city"], f"The columns should be ['name', 'city'] but are {list(result.columns)}."
    assert len(result) == 5, f"All 5 rows should remain but there are {len(result)}."


def test_in_cities():
    result = _fn("in_cities")(_people(), ["Oslo", "Lima"])
    assert result["name"].tolist() == ["Bo", "Di", "Ed"], (
        f"The people in Oslo or Lima are Bo, Di and Ed but you returned {result['name'].tolist()}."
    )


def test_oldest_first_sorts_and_renumbers():
    result = _fn("oldest_first")(_people())
    assert result["name"].tolist() == ["Cy", "Ada", "Di", "Ed", "Bo"], (
        f"Oldest first should be Cy, Ada, Di, Ed, Bo but you returned {result['name'].tolist()}."
    )
    assert result.index.tolist() == [0, 1, 2, 3, 4], (
        f"The row numbers should start again at 0 (use .reset_index(drop=True)) but are {result.index.tolist()}."
    )
