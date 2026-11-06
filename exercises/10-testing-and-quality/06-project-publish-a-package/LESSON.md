# Project: Build, Test and Package a Mini Library

*Testing and Quality · about 35 minutes*

## Why this matters

This capstone brings the course together. You will build a small, tested, installable Python library: write the code, write the tests, describe the package, and learn the commands that turn it into something other people can install. It is the same process used for libraries on PyPI, the Python package index.

## The idea

You are building **`wordkit`**, a library with three functions:

- `word_count(text)`: how many words the text has.
- `longest_word(text)`: the longest word; if several tie, the first one; `""` if there are none.
- `is_palindrome(text)`: `True` if the text reads the same both ways, ignoring capitals, spaces and punctuation (`"A man, a plan, a canal: Panama"` is one).

A project is several files, but this exercise is one file, so each file is a text value in `exercise.py`:

| Constant | Becomes the file |
|---|---|
| `PYPROJECT` | `pyproject.toml` |
| `PACKAGE_CODE` | `src/wordkit/__init__.py` |
| `TESTS` | `tests/test_wordkit.py` |
| `README` | `README.md` |

The starter also has a helper, `write_project()`. Run `python exercise.py` and it writes those four files into a real folder, so you can use real tools on your work:

```bash
python exercise.py                       # writes ./wordkit-project/
cd wordkit-project
python -m venv .venv                     # Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -e . pytest                  # install your package in editable mode
pytest                                   # run YOUR tests against YOUR code
pip install build twine
python -m build                          # makes dist/ with a .whl and a .tar.gz
twine check dist/*                       # checks the metadata
```

**Publishing.** The real index holds other people's work, so practise on **TestPyPI**, a separate sandbox. Make an account at test.pypi.org, create an API token, then run `twine upload --repository testpypi dist/*` (the username is `__token__`, the password is the token). Package names are unique across the index, so if `wordkit` is taken, choose your own, such as `wordkit-yourname`. Only upload to the real PyPI when you have something worth sharing, and never put secrets in a package.

## Try it

Work on the four files in the order: code first, then tests, then `pyproject.toml`, then the README. Run `pytest` often.

## Your turn

Fill in the four constants in `exercise.py`. The checks:

1. Write the files and read your `pyproject.toml`: the right name, a version equal to your `__version__`, `requires-python`, the setuptools build system and the `src` layout.
2. Test your library's behaviour, including the edge cases.
3. Run **your tests** against your code: at least six tests, all passing.
4. Run your tests against **broken copies** of the library. Good tests catch the bugs.
5. If the `build` tool is installed, build a real wheel from your files.

## Recap

- A library is code + tests + metadata, laid out in a standard way.
- Tests are only useful if they fail when the code is wrong.
- `pip install -e .` for development, `python -m build` to make distribution files, `twine` to upload them.
- TestPyPI is the safe place to practise publishing.

## Common mistakes

- **A version in two places that disagree** (`pyproject.toml` and `__version__`).
- **Tests that import from the wrong place**: they should use `from wordkit import ...`.
- **Uploading to the real index by accident** while practising.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/10-testing-and-quality/06-project-publish-a-package
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

PYPROJECT: copy the shape from the last lesson, using name = "wordkit", version = "0.1.0", a short description, readme, requires-python and the [build-system] and [tool.setuptools.packages.find] tables. PACKAGE_CODE needs __version__ = "0.1.0" (the same version) and three functions with docstrings.

</details>

<details><summary>Hint 2</summary>

word_count: len(text.split()). longest_word: loop over text.split() keeping the longest so far, using > so the FIRST of equally long words wins; return "" when there are no words. is_palindrome: keep only letters and digits with c.isalnum(), lowercase them, and compare the list with its reverse [::-1].

</details>

<details><summary>Hint 3</summary>

TESTS must start with from wordkit import ... and contain at least six test_ functions that pass on a correct package and also catch bugs: test empty text, extra spaces, a tie for longest word, capital letters and punctuation in palindromes. The checks run your tests against broken copies of the library.

</details>
