def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


from pathlib import Path


def test_package_name():
    package_name = _fn("package_name")
    cases = {"my-tool": "my_tool", "My Cool-Tool": "my_cool_tool", "tool!": "tool", "  Data  ": "data", "already_ok": "already_ok"}
    for given, wanted in cases.items():
        assert package_name(given) == wanted, f"package_name({given!r}) should be {wanted!r} but was {package_name(given)!r}."


def _files(project):
    return {p.relative_to(project).as_posix() for p in project.rglob("*") if p.is_file()}


def test_scaffold_creates_the_expected_files(tmp_path):
    scaffold_project = _fn("scaffold_project")
    project = scaffold_project(str(tmp_path), "my-tool")
    assert isinstance(project, Path), f"scaffold_project should return a Path but returned {project!r}."
    assert project == tmp_path / "my-tool", f"The project folder should be {tmp_path / 'my-tool'} but you returned {project}."
    expected = {"README.md", "pyproject.toml", "src/my_tool/__init__.py", "tests/test_smoke.py"}
    assert _files(project) == expected, f"The project should contain exactly {sorted(expected)} but contains {sorted(_files(project))}."


def test_scaffold_file_contents(tmp_path):
    scaffold_project = _fn("scaffold_project")
    project = scaffold_project(tmp_path, "Demo")
    assert (project / "README.md").read_text() == "# Demo\n", f"README.md should hold '# Demo' and a newline but holds {(project / 'README.md').read_text()!r}."
    expected_toml = '[project]\nname = "Demo"\nversion = "0.1.0"\nrequires-python = ">=3.11"\n'
    assert (project / "pyproject.toml").read_text() == expected_toml, f"pyproject.toml should hold:\n{expected_toml}\nbut holds:\n{(project / 'pyproject.toml').read_text()}"
    assert (project / "src" / "demo" / "__init__.py").read_text() == "", "__init__.py should be empty."
    assert (project / "tests" / "test_smoke.py").read_text() == "def test_smoke():\n    assert True\n", "test_smoke.py should hold the two-line test."


def test_scaffold_refuses_to_overwrite(tmp_path):
    import pytest

    scaffold_project = _fn("scaffold_project")
    scaffold_project(tmp_path, "demo")
    marker = tmp_path / "demo" / "README.md"
    marker.write_text("my own notes\n")
    with pytest.raises(FileExistsError):
        scaffold_project(tmp_path, "demo")
    assert marker.read_text() == "my own notes\n", "An existing project must be left untouched."
