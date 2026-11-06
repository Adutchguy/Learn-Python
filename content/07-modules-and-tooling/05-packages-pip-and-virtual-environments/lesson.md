---
title: "Packages, pip and Virtual Environments"
minutes: 20
prereqs: ["07-modules-and-tooling/04-itertools-and-random"]
concepts: ["pip", "PyPI", "package", "virtual environment", "venv", "requirements.txt", "version specifier", "pip freeze"]
local_only: true
hints:
  - "parse_requirements: for each line, strip it and cut off any text from \" #\" onwards (line.split(\"#\")[0] works). Skip the line if nothing is left. Match the name with re.match(r\"[A-Za-z0-9][A-Za-z0-9._-]*\", line).group(0); the rest of the line, with spaces removed, is the specifier."
  - "A line like \"flask >= 2.0\" gives the name flask and the specifier \">=2.0\". A line with only a name (numpy) gives the specifier \"\". Return a list of (name, specifier) tuples in the order they appear."
  - "requirements_text: for each name in sorted(versions), write name + \"==\" + version when a version is given, or just name when it is None or empty. Every line ends with a newline, so an empty dictionary gives \"\"."
---

## Why this matters

Python's real power comes from other people's code: **packages** from the Python Package Index (PyPI) such as `requests` or `pandas`. You install them with `pip`. Installing into one shared place quickly makes projects clash, so every project gets its own **virtual environment**.

This lesson needs a terminal on your own computer, so it is marked **local-only**: the commands cannot run in the browser. The coding exercise (reading and writing a `requirements.txt`) can be done anywhere.

## The idea

Create and use an environment (once per project):

```text
python -m venv .venv                 # create the environment in a folder called .venv
source .venv/bin/activate            # macOS / Linux
.venv\Scripts\Activate.ps1           # Windows PowerShell
python -m pip install requests       # install a package into THIS environment
python -m pip list                   # what is installed
python -m pip freeze > requirements.txt   # save exact versions
python -m pip install -r requirements.txt # recreate it on another machine
deactivate                           # leave the environment
```

`python -m pip` makes sure you use the pip that belongs to the `python` you are running. A `requirements.txt` has one package per line, optionally with a **version specifier**:

```text
requests==2.31.0     # exactly this version
flask>=2.0           # this version or newer
numpy                # any version
```

Never commit the `.venv` folder itself to Git; commit `requirements.txt`.

## Try it

In a terminal, create a `.venv`, activate it, and run `python -m pip list`. It should be almost empty. Install a small package, then run `pip list` again.

## Your turn

Write two functions that work with requirements text:

- `parse_requirements(text)`: return a list of `(name, specifier)` tuples, one per package, in order. Ignore blank lines, full-line comments and `# ...` comments at the end of a line. Remove spaces from the specifier: `"flask >= 2.0"` gives `("flask", ">=2.0")`, and a bare name gives an empty specifier `("numpy", "")`.
- `requirements_text(versions)`: the opposite. Given a dictionary of name to version (or `None` for any version), return the file text sorted by name, one line each: `"a==2.1\nb==1.0\n"`.

## Recap

- `pip` installs packages from PyPI; use `python -m pip`.
- One virtual environment per project keeps dependencies separate.
- `requirements.txt` records what the project needs; `pip freeze` writes it.

## Common mistakes

- **Installing without activating the environment**, so the package lands in the system Python.
- **Committing `.venv`** to Git.
- **`ModuleNotFoundError` after installing**: you installed into a different Python than the one that runs your code.
