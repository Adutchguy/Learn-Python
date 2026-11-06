---
title: "Organising a Python Project"
minutes: 20
prereqs: ["07-modules-and-tooling/05-packages-pip-and-virtual-environments"]
concepts: ["module", "package", "__init__.py", "src layout", "pyproject.toml", "__main__.py", "relative import", "pathlib"]
local_only: false
hints:
  - "package_name: lower-case the name, replace spaces and hyphens with underscores, then keep only letters, digits and underscores (a loop or a generator expression with ch.isalnum() or ch == \"_\")."
  - "scaffold_project: project = Path(root) / name. project.mkdir(parents=True) both creates the folders and raises FileExistsError by itself if the folder already exists. Then make (project / \"src\" / pkg) and (project / \"tests\") with mkdir(parents=True)."
  - "Write the files with write_text: README.md is f\"# {name}\\n\"; pyproject.toml is the four-line text from the lesson (use \\n between lines and end with a newline); src/PKG/__init__.py is empty (write_text(\"\")); tests/test_smoke.py holds the two lines def test_smoke(): and assert True. Return project."
---

## Why this matters

One file is fine for a script. Once a project has a few files, tests and dependencies, a standard layout keeps everyone (including future you) from getting lost, and makes it installable.

## The idea

A **module** is one `.py` file. A **package** is a folder of modules with an `__init__.py` file. A common modern layout:

```text
my-tool/
├── README.md
├── pyproject.toml          # project name, version, dependencies
├── src/
│   └── my_tool/            # the package: lowercase_with_underscores
│       ├── __init__.py     # can be empty
│       ├── cli.py
│       └── __main__.py     # runs with: python -m my_tool
└── tests/
    └── test_cli.py
```

Import across files with the package name: `from my_tool.cli import main`, or relatively inside the package: `from .cli import main`. The project folder may have a hyphen, but the **package** name may not (it must be a valid identifier), so `my-tool` becomes `my_tool`.

A minimal `pyproject.toml`:

```toml
[project]
name = "my-tool"
version = "0.1.0"
requires-python = ">=3.11"
```

## Try it

Sketch (on paper) the layout of the expense tracker project from Module 6. Which parts would be separate modules?

## Your turn

Write two functions:

- `package_name(project_name)`: turn a project name into a valid package name: lower-case, spaces and hyphens become underscores, other punctuation is removed. `"My Cool-Tool"` becomes `"my_cool_tool"`.
- `scaffold_project(root, name)`: create the project folder `root/name` containing exactly these files, and return its path (a `Path`):
  - `README.md` with the text `# NAME` and a newline
  - `pyproject.toml` with the four lines shown above, using `NAME` as the project name, ending with a newline
  - `src/PACKAGE/__init__.py`, empty (`PACKAGE` is `package_name(name)`)
  - `tests/test_smoke.py` containing `def test_smoke():` and `    assert True` on two lines, ending with a newline

  If the project folder already exists, raise `FileExistsError` instead of overwriting anything.

## Recap

- A module is a file; a package is a folder with `__init__.py`.
- Put code in `src/package_name/`, tests in `tests/`, metadata in `pyproject.toml`.
- Package names use underscores; project names may use hyphens.

## Common mistakes

- **A package folder without `__init__.py`** (in simple cases Python copes, but tools and imports can behave differently).
- **Circular imports**: `a.py` imports `b.py` which imports `a.py` gives `ImportError`. Move shared code into a third module.
- **Running a package file directly** instead of with `python -m my_tool.cli`, which breaks relative imports.
