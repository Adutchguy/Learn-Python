from pathlib import Path


def package_name(project_name):
    name = project_name.strip().lower().replace(" ", "_").replace("-", "_")
    return "".join(ch for ch in name if ch.isalnum() or ch == "_")


def scaffold_project(root, name):
    project = Path(root) / name
    project.mkdir(parents=True)
    pkg = package_name(name)
    (project / "src" / pkg).mkdir(parents=True)
    (project / "tests").mkdir()
    (project / "README.md").write_text(f"# {name}\n")
    (project / "pyproject.toml").write_text(
        f'[project]\nname = "{name}"\nversion = "0.1.0"\nrequires-python = ">=3.11"\n'
    )
    (project / "src" / pkg / "__init__.py").write_text("")
    (project / "tests" / "test_smoke.py").write_text("def test_smoke():\n    assert True\n")
    return project
