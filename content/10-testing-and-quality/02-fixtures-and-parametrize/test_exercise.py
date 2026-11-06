import ast
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _run_learners_file(tmp_path):
    import exercise

    source = Path(exercise.__file__).read_text(encoding="utf-8")
    target = tmp_path / "test_learner.py"
    target.write_text(source, encoding="utf-8")
    report = tmp_path / "report.xml"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={report}", str(target)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    cases = []
    if report.exists():
        for case in ET.parse(report).getroot().iter("testcase"):
            failed = case.find("failure") is not None or case.find("error") is not None
            cases.append((case.get("name"), failed))
    return source, result, cases


def _decorator_names(node):
    names = []
    for dec in node.decorator_list:
        target = dec.func if isinstance(dec, ast.Call) else dec
        names.append(ast.unparse(target))
    return names


def test_your_file_runs_and_everything_passes(tmp_path):
    source, result, cases = _run_learners_file(tmp_path)
    assert cases, f"pytest found no tests in your file. Output:\n{result.stdout[-1200:]}{result.stderr[-600:]}"
    failed = [name for name, bad in cases if bad]
    assert not failed, f"These tests fail: {failed}. Output:\n{result.stdout[-1500:]}"


def test_you_defined_a_stack_fixture(tmp_path):
    source, _, _ = _run_learners_file(tmp_path)
    tree = ast.parse(source)
    fixtures = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and any(d.endswith("fixture") for d in _decorator_names(node))
    ]
    assert "stack" in fixtures, "Define a fixture named stack: put @pytest.fixture above def stack():"


def test_at_least_two_tests_use_the_fixture(tmp_path):
    source, _, _ = _run_learners_file(tmp_path)
    tree = ast.parse(source)
    users = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name.startswith("test_")
        and "stack" in [arg.arg for arg in node.args.args]
    ]
    assert len(users) >= 2, f"Write at least 2 tests that take the parameter stack (found {len(users)})."


def test_parametrize_runs_at_least_three_cases(tmp_path):
    _, _, cases = _run_learners_file(tmp_path)
    parametrized = [name for name, _ in cases if "[" in name]
    assert len(parametrized) >= 3, f"Use @pytest.mark.parametrize with at least 3 sets of values (pytest ran {len(parametrized)} parametrized cases)."
