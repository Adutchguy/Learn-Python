import ast
import importlib.util
import os
import subprocess
import sys
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

REFERENCE = '"""wordkit: tiny helpers for working with text."""\n\n__version__ = "0.1.0"\n\n\ndef word_count(text):\n    """Return how many words the text contains."""\n    return len(text.split())\n\n\ndef longest_word(text):\n    """Return the longest word (the first one if tied), or an empty string."""\n    longest = ""\n    for word in text.split():\n        if len(word) > len(longest):\n            longest = word\n    return longest\n\n\ndef is_palindrome(text):\n    """Return True if the text reads the same both ways, ignoring case and punctuation."""\n    characters = [c.lower() for c in text if c.isalnum()]\n    return characters == characters[::-1]\n'


def _constant(name):
    import exercise

    value = getattr(exercise, name, None)
    assert isinstance(value, str), f"{name} should be a string"
    return value.lstrip("\n")


def _write(root, package_code, pyproject=None, tests=None, readme=None):
    files = {
        "pyproject.toml": pyproject if pyproject is not None else _constant("PYPROJECT"),
        "README.md": readme if readme is not None else _constant("README"),
        "src/wordkit/__init__.py": package_code,
        "tests/test_wordkit.py": tests if tests is not None else _constant("TESTS"),
    }
    for relative, content in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def _load_library(root):
    spec = importlib.util.spec_from_file_location("wordkit_under_test", root / "src" / "wordkit" / "__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_tests(root):
    report = root / "report.xml"
    env = dict(os.environ, PYTHONPATH=str(root / "src"))
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={report}", str(root / "tests")],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
    )
    cases = []
    if report.exists():
        for case in ET.parse(report).getroot().iter("testcase"):
            failed = case.find("failure") is not None or case.find("error") is not None
            cases.append((case.get("name"), failed))
    return result, cases


def test_pyproject_metadata(tmp_path):
    code = _constant("PACKAGE_CODE")
    _write(tmp_path, code)
    try:
        data = tomllib.loads((tmp_path / "pyproject.toml").read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise AssertionError(f"PYPROJECT is not valid TOML: {exc}")
    project = data.get("project", {})
    assert project.get("name") == "wordkit", f"[project] name should be 'wordkit', found {project.get('name')!r}"
    namespace = {}
    exec(compile(code, "__init__.py", "exec"), namespace)
    assert namespace.get("__version__") == project.get("version"), (
        f"The version in pyproject.toml ({project.get('version')!r}) must equal __version__ in your package ({namespace.get('__version__')!r})"
    )
    assert str(project.get("description", "")).strip(), "[project] needs a description"
    assert str(project.get("requires-python", "")).startswith(">="), "[project] needs requires-python, for example '>=3.11'"
    assert data.get("build-system", {}).get("build-backend") == "setuptools.build_meta", "[build-system] build-backend should be 'setuptools.build_meta'"
    assert "setuptools" in " ".join(data.get("build-system", {}).get("requires", [])), "[build-system] requires should include setuptools"
    assert data.get("tool", {}).get("setuptools", {}).get("packages", {}).get("find", {}).get("where") == ["src"], "add [tool.setuptools.packages.find] with where = ['src']"


def test_readme_has_a_title_and_an_example():
    readme = _constant("README")
    assert readme.startswith("# wordkit"), "README should start with the title '# wordkit'"
    assert len(readme.strip().splitlines()) >= 4, "README should describe the library and include a short example"


def test_library_word_count_and_longest_word(tmp_path):
    _write(tmp_path, _constant("PACKAGE_CODE"))
    lib = _load_library(tmp_path)
    assert lib.word_count("one two three") == 3, "word_count('one two three') should be 3"
    assert lib.word_count("") == 0, "word_count('') should be 0"
    assert lib.word_count("  a   b ") == 2, "extra spaces should not create extra words"
    assert lib.longest_word("a quick brown fox") == "quick", "longest_word('a quick brown fox') should be 'quick'"
    assert lib.longest_word("aa bb cc") == "aa", "with a tie, the first longest word wins"
    assert lib.longest_word("") == "", "longest_word('') should be ''"


def test_library_is_palindrome(tmp_path):
    _write(tmp_path, _constant("PACKAGE_CODE"))
    lib = _load_library(tmp_path)
    assert lib.is_palindrome("Racecar") is True, "capital letters should be ignored"
    assert lib.is_palindrome("A man, a plan, a canal: Panama") is True, "spaces and punctuation should be ignored"
    assert lib.is_palindrome("python") is False, "'python' is not a palindrome"
    assert lib.is_palindrome("") is True, "empty text reads the same both ways"


def test_every_function_has_a_docstring(tmp_path):
    tree = ast.parse(_constant("PACKAGE_CODE"))
    names = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    assert {"word_count", "longest_word", "is_palindrome"} <= set(names), "PACKAGE_CODE must define word_count, longest_word and is_palindrome"
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            assert ast.get_docstring(node), f"{node.name} needs a docstring"


def test_your_tests_pass_on_your_code(tmp_path):
    _write(tmp_path, _constant("PACKAGE_CODE"))
    result, cases = _run_tests(tmp_path)
    assert cases, f"pytest found no tests in TESTS. Output:\n{result.stdout[-1200:]}{result.stderr[-600:]}"
    assert len(cases) >= 6, f"Write at least 6 tests (found {len(cases)})."
    failed = [name for name, bad in cases if bad]
    assert not failed, f"These of your tests fail against your own code: {failed}.\n{result.stdout[-1500:]}"


MUTANTS = {
    "counts words by splitting on single spaces": ("len(text.split())", "len(text.split(' '))"),
    "lets a later word win a tie for longest": ("if len(word) > len(longest):", "if len(word) >= len(longest):"),
    "forgets to ignore capital letters in palindromes": ("c.lower() for c in text if c.isalnum()", "c for c in text if c.isalnum()"),
    "forgets to ignore punctuation in palindromes": ("for c in text if c.isalnum()", "for c in text if c != ' '"),
}


def test_your_tests_catch_broken_libraries(tmp_path):
    reference_root = tmp_path / "reference"
    _write(reference_root, REFERENCE)
    result, cases = _run_tests(reference_root)
    failed = [name for name, bad in cases if bad]
    assert cases and not failed, f"Your tests fail even on a correct wordkit, so one of them expects the wrong thing: {failed}\n{result.stdout[-1200:]}"
    for index, (description, (old, new)) in enumerate(MUTANTS.items()):
        assert old in REFERENCE, f"internal error: {old!r} not in the reference library"
        root = tmp_path / f"mutant{index}"
        _write(root, REFERENCE.replace(old, new))
        _, mutant_cases = _run_tests(root)
        assert any(bad for _, bad in mutant_cases), f"Your tests did not notice a wordkit that {description}. Add a test for that case."


def test_a_wheel_can_be_built(tmp_path):
    if importlib.util.find_spec("build") is None or importlib.util.find_spec("setuptools") is None:
        import pytest

        pytest.skip("The build tool is not installed (pip install build); try the build in your terminal.")
    _write(tmp_path, _constant("PACKAGE_CODE"))
    result = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation", "--outdir", str(tmp_path / "dist"), str(tmp_path)],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 0, f"python -m build failed:\n{result.stdout[-1500:]}{result.stderr[-800:]}"
    wheels = list((tmp_path / "dist").glob("wordkit-*.whl"))
    assert wheels, "no wordkit wheel was produced in dist/"
