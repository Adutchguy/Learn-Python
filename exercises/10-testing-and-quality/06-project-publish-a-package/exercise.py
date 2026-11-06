import json
from pathlib import Path

PYPROJECT = """
# Write pyproject.toml here: build-system, project metadata, src layout.
"""

PACKAGE_CODE = '''
"""wordkit: tiny helpers for working with text."""

# Add __version__ and the three functions:
# word_count(text), longest_word(text), is_palindrome(text)
'''

TESTS = '''
# Write at least six tests. Start with:
# from wordkit import is_palindrome, longest_word, word_count
'''

README = """# wordkit

(Describe what the library does and show an example.)
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
