def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _cls(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a class called {name}. Start it with: class {name}:"
    cls = getattr(exercise, name)
    assert isinstance(cls, type), f"{name} should be a class, but it is {cls!r}."
    return cls


def test_vector_repr():
    Vector = _cls("Vector")
    assert repr(Vector(1, 2)) == "Vector(1, 2)", f"repr(Vector(1, 2)) should be 'Vector(1, 2)' but was {repr(Vector(1, 2))!r}."
    assert str(Vector(1, 2)) == "Vector(1, 2)", f"str(Vector(1, 2)) falls back to __repr__ and should be 'Vector(1, 2)' but was {str(Vector(1, 2))!r}."


def test_vector_equality():
    Vector = _cls("Vector")
    assert Vector(1, 2) == Vector(1, 2), "Vector(1, 2) == Vector(1, 2) should be True."
    assert Vector(1, 2) != Vector(2, 1), "Vector(1, 2) and Vector(2, 1) are different vectors."
    assert (Vector(1, 2) == (1, 2)) is False, "Comparing a Vector with a tuple should give False, not crash. Return NotImplemented when other is not a Vector."


def test_vector_add_and_multiply():
    Vector = _cls("Vector")
    assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6), f"Vector(1, 2) + Vector(3, 4) should be Vector(4, 6) but was {Vector(1, 2) + Vector(3, 4)!r}."
    assert Vector(1, 2) * 3 == Vector(3, 6), f"Vector(1, 2) * 3 should be Vector(3, 6) but was {Vector(1, 2) * 3!r}."
    a = Vector(1, 1)
    a + Vector(5, 5)
    assert a == Vector(1, 1), "Adding should create a new Vector and leave the original unchanged."


def test_version_str():
    Version = _cls("Version")
    assert str(Version("1.10.2")) == "1.10.2", f"str(Version('1.10.2')) should be '1.10.2' but was {str(Version('1.10.2'))!r}."


def test_version_equality():
    Version = _cls("Version")
    assert Version("1.2.3") == Version("1.2.3"), "Two Versions with the same numbers should be equal."
    assert Version("1.2.3") != Version("1.2.4"), "Different numbers should not be equal."
    assert (Version("1.2") == "1.2") is False, "Comparing a Version with text should give False, not crash."


def test_version_ordering_is_numeric():
    Version = _cls("Version")
    assert Version("1.10.0") > Version("1.2.0"), "1.10.0 is a newer version than 1.2.0 (compare the numbers, not the text)."
    assert Version("1.2.0") < Version("1.2.1"), "1.2.0 is older than 1.2.1."
    assert not (Version("2.0") < Version("1.9")), "2.0 is newer than 1.9."


def test_sorted_versions():
    Version = _cls("Version")
    versions = [Version(t) for t in ["1.10.0", "1.2.0", "1.9.5", "1.2.10"]]
    result = [str(v) for v in sorted(versions)]
    assert result == ["1.2.0", "1.2.10", "1.9.5", "1.10.0"], f"sorted() should order the versions as ['1.2.0', '1.2.10', '1.9.5', '1.10.0'] but gave {result!r}."
    assert str(max(versions)) == "1.10.0", f"max() should find 1.10.0 but found {max(versions)}."
