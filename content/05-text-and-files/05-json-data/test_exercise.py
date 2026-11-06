def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_to_json_is_indented_and_sorted():
    result = _fn("to_json")({"b": 1, "a": [1, 2]})
    want = '{\n  "a": [\n    1,\n    2\n  ],\n  "b": 1\n}'
    assert result == want, f"to_json should use indent=2 and sort_keys=True. Expected:\n{want}\nbut got:\n{result}"


def test_to_json_handles_special_values():
    result = _fn("to_json")({"ok": True, "nothing": None})
    want = '{\n  "nothing": null,\n  "ok": true\n}'
    assert result == want, f"True and None should become true and null. Expected:\n{want}\nbut got:\n{result}"


def test_save_json_writes_a_file(tmp_path):
    import json

    path = tmp_path / "settings.json"
    data = {"name": "Ada", "scores": [90, 85]}
    _fn("save_json")(path, data)
    assert path.exists(), "save_json should create the file."
    assert json.loads(path.read_text()) == data, f"The file should contain the data as JSON but contains {path.read_text()!r}."


def test_load_json_reads_a_file(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text('{"theme": "dark", "size": 12}')
    result = _fn("load_json")(path, {})
    assert result == {"theme": "dark", "size": 12}, f"load_json should return the saved data but returned {result!r}."


def test_load_json_returns_default_when_missing(tmp_path):
    result = _fn("load_json")(tmp_path / "missing.json", {"theme": "light"})
    assert result == {"theme": "light"}, f"For a missing file load_json should return the default {{'theme': 'light'}} but returned {result!r}."


def test_save_then_load_round_trip(tmp_path):
    path = tmp_path / "round.json"
    data = {"list": [1, 2, 3], "flag": False, "none": None, "text": "héllo"}
    _fn("save_json")(path, data)
    result = _fn("load_json")(path, None)
    assert result == data, f"Saving {data!r} and loading it back should give the same data but gave {result!r}."
