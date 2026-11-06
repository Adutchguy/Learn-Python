def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_parse_requirements_simple_lines():
    parse_requirements = _fn("parse_requirements")
    text = "requests==2.31.0\nflask >= 2.0\nnumpy\n"
    expected = [("requests", "==2.31.0"), ("flask", ">=2.0"), ("numpy", "")]
    assert parse_requirements(text) == expected, f"Expected {expected!r} but got {parse_requirements(text)!r}."


def test_parse_requirements_skips_comments_and_blank_lines():
    parse_requirements = _fn("parse_requirements")
    text = "# my project\n\npytest>=8  # for tests\n   \nrich\n"
    expected = [("pytest", ">=8"), ("rich", "")]
    assert parse_requirements(text) == expected, f"Expected {expected!r} but got {parse_requirements(text)!r}. Comments and blank lines are not packages."


def test_parse_requirements_names_with_dashes_and_dots():
    parse_requirements = _fn("parse_requirements")
    assert parse_requirements("python-dateutil~=2.8\nzope.interface") == [("python-dateutil", "~=2.8"), ("zope.interface", "")], "Names may contain dashes and dots."


def test_parse_requirements_empty_text():
    parse_requirements = _fn("parse_requirements")
    assert parse_requirements("") == [], "Empty text has no packages."


def test_requirements_text_sorted_with_versions():
    requirements_text = _fn("requirements_text")
    result = requirements_text({"b": "1.0", "a": "2.1"})
    assert result == "a==2.1\nb==1.0\n", f"Expected 'a==2.1\\nb==1.0\\n' (sorted by name) but got {result!r}."


def test_requirements_text_without_a_version():
    requirements_text = _fn("requirements_text")
    result = requirements_text({"rich": None, "attrs": "23.1"})
    assert result == "attrs==23.1\nrich\n", f"A package with no version is just its name. Expected 'attrs==23.1\\nrich\\n' but got {result!r}."
    assert requirements_text({}) == "", "No packages gives empty text."
