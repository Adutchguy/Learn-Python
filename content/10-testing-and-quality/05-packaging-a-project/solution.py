import json
import re
from pathlib import Path


def pyproject_text(name, version, description, dependencies):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        raise ValueError(f"invalid project name: {name!r}")
    return (
        "[build-system]\n"
        'requires = ["setuptools>=68"]\n'
        'build-backend = "setuptools.build_meta"\n'
        "\n"
        "[project]\n"
        f"name = {json.dumps(name)}\n"
        f"version = {json.dumps(version)}\n"
        f"description = {json.dumps(description)}\n"
        'readme = "README.md"\n'
        'requires-python = ">=3.11"\n'
        f"dependencies = {json.dumps(list(dependencies))}\n"
        "\n"
        "[tool.setuptools.packages.find]\n"
        'where = ["src"]\n'
    )


def create_project(root, name, version, description, dependencies):
    root = Path(root)
    if (root / "pyproject.toml").exists():
        raise FileExistsError(f"{root} already contains a project")
    text = pyproject_text(name, version, description, dependencies)
    package = name.lower().replace("-", "_").replace(".", "_")
    files = {
        "pyproject.toml": text,
        "README.md": f"# {name}\n\n{description}\n",
        f"src/{package}/__init__.py": f'"""{description}"""\n\n__version__ = {json.dumps(version)}\n',
        f"tests/test_{package}.py": (
            f"from {package} import __version__\n\n\n"
            "def test_version():\n"
            f"    assert __version__ == {json.dumps(version)}\n"
        ),
    }
    for relative, content in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return sorted(files)
