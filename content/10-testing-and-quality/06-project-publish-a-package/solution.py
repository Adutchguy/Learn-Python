import json
from pathlib import Path

PYPROJECT = """
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "wordkit"
version = "0.1.0"
description = "Tiny helpers for working with text."
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[tool.setuptools.packages.find]
where = ["src"]
"""

PACKAGE_CODE = '''
"""wordkit: tiny helpers for working with text."""

__version__ = "0.1.0"


def word_count(text):
    """Return how many words the text contains."""
    return len(text.split())


def longest_word(text):
    """Return the longest word (the first one if tied), or an empty string."""
    longest = ""
    for word in text.split():
        if len(word) > len(longest):
            longest = word
    return longest


def is_palindrome(text):
    """Return True if the text reads the same both ways, ignoring case and punctuation."""
    characters = [c.lower() for c in text if c.isalnum()]
    return characters == characters[::-1]
'''

TESTS = '''
import pytest
from wordkit import __version__, is_palindrome, longest_word, word_count


def test_word_count():
    assert word_count("one two three") == 3


def test_word_count_of_empty_text():
    assert word_count("") == 0


def test_word_count_ignores_extra_spaces():
    assert word_count("  a   b ") == 2


def test_longest_word():
    assert longest_word("a quick brown fox") == "quick"


def test_longest_word_tie_gives_the_first():
    assert longest_word("aa bb cc") == "aa"


def test_longest_word_of_empty_text():
    assert longest_word("") == ""


def test_palindrome_ignores_case_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama")


def test_not_a_palindrome():
    assert not is_palindrome("python")


def test_version_is_text():
    assert isinstance(__version__, str)
'''

README = """# wordkit

Tiny helpers for working with text.

```python
from wordkit import word_count
word_count("hello big world")   # 3
```
"""


def write_project(folder="wordkit-project"):
    """Write the four constants as real files so you can try pip, pytest and build."""
    root = Path(folder)
    files = {
        "pyproject.toml": PYPROJECT,
        "README.md": README,
        "src/wordkit/__init__.py": PACKAGE_CODE,
        "tests/test_wordkit.py": TESTS,
    }
    for relative, content in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"Wrote {len(files)} files into {root}/")


if __name__ == "__main__":
    write_project()
