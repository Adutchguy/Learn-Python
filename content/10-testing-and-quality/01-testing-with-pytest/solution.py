import pytest


def slugify(text):
    """Turn a title into a URL slug: lowercase words joined by hyphens."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return "-".join(text.lower().split())


def test_joins_words_with_hyphens():
    assert slugify("Hello World") == "hello-world"


def test_lowercases_everything():
    assert slugify("PYTHON Is FUN") == "python-is-fun"


def test_trims_spaces_at_both_ends():
    assert slugify("  padded  ") == "padded"


def test_collapses_repeated_spaces():
    assert slugify("a    b") == "a-b"


def test_rejects_non_text():
    with pytest.raises(TypeError):
        slugify(42)
