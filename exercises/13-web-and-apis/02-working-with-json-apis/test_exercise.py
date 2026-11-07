def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_extract_names():
    text = '{"results": [{"name": "Ada", "age": 36}, {"name": "Bo"}, {"name": "Cy"}]}'
    result = _fn("extract_names")(text)
    assert result == ["Ada", "Bo", "Cy"], f"Expected ['Ada', 'Bo', 'Cy'] but got {result}."


def test_extract_names_from_an_empty_result():
    result = _fn("extract_names")('{"results": []}')
    assert result == [], f"No results should give an empty list but gave {result}."


def test_safe_get_follows_nested_keys():
    data = {"a": {"b": {"c": 5}}}
    assert _fn("safe_get")(data, "a", "b", "c") == 5, "safe_get(data, 'a', 'b', 'c') should find 5."
    assert _fn("safe_get")(data, "a", "b") == {"c": 5}, "safe_get(data, 'a', 'b') should find the inner dict."


def test_safe_get_returns_the_default_for_missing_keys():
    data = {"a": {"b": 1}}
    assert _fn("safe_get")(data, "a", "x") is None, "A missing key should give None by default."
    assert _fn("safe_get")(data, "z", "b", default=0) == 0, "A missing first key should give the default (0)."


def test_safe_get_survives_null_and_non_dicts():
    data = {"stats": None, "name": "Ada", "list": [1, 2]}
    assert _fn("safe_get")(data, "stats", "wins", default=0) == 0, "A null (None) in the middle should give the default, not crash."
    assert _fn("safe_get")(data, "name", "first", default="?") == "?", "Digging into a string should give the default, not crash."
    assert _fn("safe_get")(data, "list", "x", default="?") == "?", "Digging into a list with a text key should give the default."


def test_safe_get_keeps_a_value_of_none_or_zero():
    data = {"a": 0, "b": None}
    assert _fn("safe_get")(data, "a", default=99) == 0, "A real value of 0 must be returned, not replaced by the default."


def test_all_pages_collects_every_item():
    pages = {1: {"items": ["a", "b"], "next_page": 2}, 2: {"items": ["c"], "next_page": 3}, 3: {"items": ["d", "e"], "next_page": None}}
    asked = []

    def fetch(number):
        asked.append(number)
        return pages[number]

    result = _fn("all_pages")(fetch)
    assert result == ["a", "b", "c", "d", "e"], f"Expected all five items in order but got {result}."
    assert asked == [1, 2, 3], f"The pages should be requested as 1, 2, 3 (following next_page) but were {asked}."


def test_all_pages_with_a_single_page():
    result = _fn("all_pages")(lambda number: {"items": [number], "next_page": None})
    assert result == [1], f"A single page should give its items, [1], but gave {result}."


def test_all_pages_stops_a_runaway_server():
    import pytest

    with pytest.raises(RuntimeError):
        _fn("all_pages")(lambda number: {"items": [number], "next_page": number + 1}, max_pages=5)


def test_describe_error():
    describe = _fn("describe_error")
    assert describe(200, "{}") == "OK", "A 2xx status should give 'OK'."
    assert describe(204, "") == "OK", "204 is a success too, even with an empty body."
    got = describe(429, '{"message": "Rate limit exceeded"}')
    assert got == "Request problem (429): Rate limit exceeded", f"A 4xx with a JSON message should use that message. Got {got!r}."
    got = describe(404, "<html>Not here</html>")
    assert got == "Request problem (404): <html>Not here</html>", f"When the body is not JSON, use the body text. Got {got!r}."
    got = describe(503, '{"message": "busy"}')
    assert got == "Server problem (503): try again later", f"A 5xx should say 'Server problem (<status>): try again later'. Got {got!r}."
