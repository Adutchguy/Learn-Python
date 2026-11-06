def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import tomllib

import pytest


def test_pyproject_text_is_valid_toml_with_the_right_values():
    pyproject_text = _fn("pyproject_text")
    text = pyproject_text("text-tools", "0.1.0", 'Helpers for "text".', ["requests>=2", "rich"])
    data = tomllib.loads(text)
    project = data["project"]
    assert project["name"] == "text-tools", f"[project] name should be 'text-tools', got {project.get('name')!r}"
    assert project["version"] == "0.1.0", f"[project] version should be '0.1.0', got {project.get('version')!r}"
    assert project["description"] == 'Helpers for "text".', "the description should survive quoting, including the double quotes"
    assert project["dependencies"] == ["requests>=2", "rich"], f"dependencies should be listed, got {project.get('dependencies')!r}"
    assert project["requires-python"] == ">=3.11", "requires-python should be '>=3.11'"
    assert project["readme"] == "README.md", "readme should be 'README.md'"


def test_pyproject_text_build_system_and_src_layout():
    pyproject_text = _fn("pyproject_text")
    data = tomllib.loads(pyproject_text("x", "1.0", "d", []))
    assert data["build-system"]["requires"] == ["setuptools>=68"], "[build-system] requires should be ['setuptools>=68']"
    assert data["build-system"]["build-backend"] == "setuptools.build_meta", "build-backend should be 'setuptools.build_meta'"
    assert data["tool"]["setuptools"]["packages"]["find"]["where"] == ["src"], "add [tool.setuptools.packages.find] with where = ['src']"
    assert data["project"]["dependencies"] == [], "an empty dependency list should be written as []"


def test_pyproject_text_rejects_bad_names():
    pyproject_text = _fn("pyproject_text")
    for bad in ["", "has space", "-leading", "semi;colon", "ünï"]:
        with pytest.raises(ValueError):
            pyproject_text(bad, "1.0", "d", [])


def test_create_project_makes_the_layout(tmp_path):
    create_project = _fn("create_project")
    created = create_project(tmp_path / "proj", "text-tools", "0.2.0", "Text helpers", ["rich"])
    assert created == [
        "README.md",
        "pyproject.toml",
        "src/text_tools/__init__.py",
        "tests/test_text_tools.py",
    ], f"create_project should return the four relative paths, sorted; got {created!r}"
    root = tmp_path / "proj"
    for relative in created:
        assert (root / relative).is_file(), f"{relative} should exist as a file"
    data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["name"] == "text-tools", "the pyproject.toml on disk should hold the project name"


def test_create_project_package_exposes_the_version(tmp_path):
    create_project = _fn("create_project")
    create_project(tmp_path / "p", "my-lib", "3.1.4", "A library", [])
    init = (tmp_path / "p" / "src" / "my_lib" / "__init__.py").read_text(encoding="utf-8")
    namespace = {}
    exec(compile(init, "__init__.py", "exec"), namespace)
    assert namespace.get("__version__") == "3.1.4", "src/my_lib/__init__.py should define __version__ = '3.1.4'"
    test_source = (tmp_path / "p" / "tests" / "test_my_lib.py").read_text(encoding="utf-8")
    compile(test_source, "test_my_lib.py", "exec")
    assert "def test_" in test_source, "the generated test file should contain a test function"


def test_create_project_refuses_to_overwrite(tmp_path):
    create_project = _fn("create_project")
    create_project(tmp_path / "again", "demo", "1.0", "d", [])
    with pytest.raises(FileExistsError):
        create_project(tmp_path / "again", "demo", "1.0", "d", [])
