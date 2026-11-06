import pytest


def slugify(text):
    """Turn a title into a URL slug: lowercase words joined by hyphens."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return "-".join(text.lower().split())


# Write at least four tests below. Each one is a function starting with test_
