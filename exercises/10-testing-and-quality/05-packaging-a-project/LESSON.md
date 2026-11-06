# Packaging: pyproject.toml and the src Layout

*Testing and Quality · about 20 minutes*

## Why this matters

A single `.py` file is easy to share. A real project, with several modules, tests and dependencies, needs a standard shape so anyone can install it with `pip install .` and tools know how to build it. Python's standard answer is a file called **`pyproject.toml`**, plus a tidy folder layout.

## The idea

The common **src layout**:

```
text-tools/
├── pyproject.toml
├── README.md
├── src/
│   └── text_tools/
│       └── __init__.py
└── tests/
    └── test_text_tools.py
```

Putting the code under `src/` stops tests from accidentally importing the folder instead of the installed package. Note the two spellings: the project (distribution) is `text-tools`, but the importable package must be a valid Python name, `text_tools`.

`pyproject.toml` is written in **TOML**, a simple settings format: `key = value` lines grouped under `[table]` headings. Python 3.11 can read it with the `tomllib` module.

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "text-tools"
version = "0.1.0"
description = "Little helpers for text."
readme = "README.md"
requires-python = ">=3.11"
dependencies = ["requests>=2"]

[tool.setuptools.packages.find]
where = ["src"]
```

- `[build-system]` says which tool builds the package.
- `[project]` is the metadata: name, version, what it needs.
- `dependencies` lists the packages yours needs. Add version limits only when you must.

On your own computer, `pip install -e .` installs the project in "editable" mode while you work, and `python -m build` makes the files you could upload to an index (you will do that in the capstone).

Expose the version in one place the code can also read: `__version__ = "0.1.0"` in `__init__.py`.

## Try it

Run the example with `tomllib.loads(text)` and print `data["project"]["name"]` to see that TOML becomes a normal dictionary.

## Your turn

Write two functions:

- `pyproject_text(name, version, description, dependencies)` returns the text of a `pyproject.toml` like the one above. It raises `ValueError` if `name` is not made of letters, digits, `.`, `_` or `-` (starting with a letter or digit). Quote text values with `json.dumps`, which produces valid TOML strings.
- `create_project(root, name, version, description, dependencies)` creates the folder layout under `root` with four files: `pyproject.toml`, `README.md`, `src/<package>/__init__.py` (a docstring and `__version__`) and `tests/test_<package>.py` (a test that checks `__version__`). It raises `FileExistsError` if `root` already has a `pyproject.toml`, and returns the sorted list of created file paths, relative to `root`, written with `/`.

## Recap

- `pyproject.toml` holds the build settings and the project metadata.
- The `src` layout keeps importable code apart from tests.
- The project name may contain `-`; the package name uses `_`.
- `tomllib` reads TOML; `pip install -e .` and `python -m build` use it.

## Common mistakes

- **Using the project name as the import name** when it contains hyphens.
- **Forgetting `__init__.py`**, so the package is not found.
- **Hard-coding the version in several places** so they drift apart.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/10-testing-and-quality/05-packaging-a-project
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

pyproject_text: check the name first with re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name) and raise ValueError if it does not match. Then build the text with f-strings, using json.dumps(value) around each text value so it gets quotes. json.dumps(list) makes a valid TOML list.

</details>

<details><summary>Hint 2</summary>

The text needs three tables: [build-system] with requires = ["setuptools>=68"] and build-backend = "setuptools.build_meta"; [project] with name, version, description, readme = "README.md", requires-python = ">=3.11" and dependencies; and [tool.setuptools.packages.find] with where = ["src"].

</details>

<details><summary>Hint 3</summary>

create_project: root = Path(root); if (root / "pyproject.toml").exists() raise FileExistsError. The package folder is name.lower().replace("-", "_"). Make src/<pkg> and tests with mkdir(parents=True, exist_ok=True), write the four files, and return sorted(relative paths as text) such as "src/text_tools/__init__.py".

</details>
