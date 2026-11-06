"""In-browser runner for Learn-Python lessons (runs inside Pyodide).

It does two jobs:

* ``run_program(source, stdin_text)``: run the learner's code and capture what it prints.
* ``run_tests(source, tests_source)``: run a lesson's ``test_exercise.py`` against the
  learner's code and report which checks passed.

Lesson tests are ordinary pytest-style functions, so the very same file is run by real
pytest in the local track. Real pytest is too heavy to ship to a browser, so this module
implements the small slice of it that lesson tests are allowed to use:

* plain ``test_*`` functions with ``assert`` statements
* the ``capsys``, ``monkeypatch`` and ``tmp_path`` fixtures (a subset of each)
* ``pytest.raises``, ``pytest.approx`` and ``pytest.fail``

Every test starts with a fresh ``import exercise`` that runs the learner's code, matching
``exercises/conftest.py``. Both functions return JSON strings so that they cross the
JavaScript boundary as plain text.
"""

from __future__ import annotations

import builtins
import contextlib
import importlib
import importlib.abc
import importlib.util
import inspect
import io
import json
import linecache
import os
import pathlib
import re
import shutil
import sys
import tempfile
import traceback
import types
from collections import namedtuple

EXERCISE_FILE = "exercise.py"
TEST_FILE = "test_exercise.py"
OUTPUT_LIMIT = 200_000  # characters a learner program may print before we stop it

NO_INPUT_MESSAGE = (
    "Your program asked for input but there is none left. Type your input in the "
    "Input box (one line for each input() call) and run again."
)


# ---------------------------------------------------------------------------
# Output capture and the input() shim
# ---------------------------------------------------------------------------


class _BoundedBuffer(io.StringIO):
    """A StringIO that stops runaway programs (e.g. ``while True: print(...)``)."""

    def write(self, text):
        if self.tell() + len(text) > OUTPUT_LIMIT:
            raise RuntimeError(
                f"Your program printed more than {OUTPUT_LIMIT:,} characters, so it was stopped. "
                "Is a loop never ending?"
            )
        return super().write(text)


def _make_input(lines):
    queue = list(lines)

    def fake_input(prompt=""):
        sys.stdout.write(str(prompt))
        if not queue:
            raise EOFError(NO_INPUT_MESSAGE)
        line = queue.pop(0)
        sys.stdout.write(line + "\n")  # echo, like a terminal does
        return line

    return fake_input


@contextlib.contextmanager
def _sandbox(stdin_lines, out, err):
    old = sys.stdout, sys.stderr, builtins.input
    sys.stdout, sys.stderr = out, err
    builtins.input = _make_input(stdin_lines)
    try:
        yield
    finally:
        sys.stdout, sys.stderr, builtins.input = old


# ---------------------------------------------------------------------------
# Friendly error text
# ---------------------------------------------------------------------------


def _register_source(source):
    # Lets tracebacks show the learner's own lines of code.
    linecache.cache[EXERCISE_FILE] = (len(source), None, source.splitlines(True), EXERCISE_FILE)


def _format_error(exc):
    """A traceback that only mentions the learner's own code."""
    if isinstance(exc, SyntaxError):
        return "".join(traceback.format_exception_only(type(exc), exc))
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == EXERCISE_FILE]
    lines = []
    if frames:
        lines.append("Traceback (most recent call last):\n")
        lines.extend(traceback.format_list(frames))
    lines.extend(traceback.format_exception_only(type(exc), exc))
    return "".join(lines)


def _explain_test_failure(exc):
    if isinstance(exc, SyntaxError) and exc.filename == EXERCISE_FILE:
        return "Your program has a syntax error:\n" + _format_error(exc)
    frames = traceback.extract_tb(exc.__traceback__)
    if any(f.filename == EXERCISE_FILE for f in frames):
        return "Your program stopped with an error:\n" + _format_error(exc)
    if isinstance(exc, _UnsupportedFixture):
        return str(exc)
    if isinstance(exc, AssertionError):
        return str(exc) or "This check failed."
    return f"Something unexpected went wrong while checking: {type(exc).__name__}: {exc}"


# ---------------------------------------------------------------------------
# Running a program
# ---------------------------------------------------------------------------


def run_program(source, stdin_text=""):
    out = _BoundedBuffer()
    error = None
    _register_source(source)
    namespace = {"__name__": "__main__", "__file__": EXERCISE_FILE}
    with _sandbox(str(stdin_text).splitlines(), out, out):
        try:
            exec(compile(source, EXERCISE_FILE, "exec", dont_inherit=True), namespace)
        except SystemExit:
            pass
        except BaseException as exc:  # noqa: BLE001 - we report every kind of failure
            error = _format_error(exc)
    return json.dumps({"output": out.getvalue(), "error": error})


# ---------------------------------------------------------------------------
# A tiny slice of pytest
# ---------------------------------------------------------------------------


class _UnsupportedFixture(Exception):
    pass


_NOTSET = object()
_CaptureResult = namedtuple("CaptureResult", "out err")


class _Capsys:
    def __init__(self, out, err):
        self._out, self._err = out, err

    def readouterr(self):
        result = _CaptureResult(self._out.getvalue(), self._err.getvalue())
        for stream in (self._out, self._err):
            stream.seek(0)
            stream.truncate(0)
        return result


class _Chdir:
    def __init__(self, old):
        self.old = old


class _MonkeyPatch:
    def __init__(self):
        self._undo = []

    def chdir(self, path):
        self._undo.append(_Chdir(os.getcwd()))
        os.chdir(os.fspath(path))

    def setattr(self, target, name=_NOTSET, value=_NOTSET, raising=True):
        if isinstance(target, str) and value is _NOTSET:  # setattr("module.attr", value)
            value = name
            module_path, _, attr = target.rpartition(".")
            if not module_path:
                raise TypeError("use monkeypatch.setattr('module.attribute', value)")
            target, name = importlib.import_module(module_path), attr
        elif value is _NOTSET:
            raise TypeError("monkeypatch.setattr needs (obj, name, value) or ('module.attr', value)")
        old = getattr(target, name, _NOTSET)
        if raising and old is _NOTSET:
            raise AttributeError(f"{target!r} has no attribute {name!r}")
        self._undo.append((target, name, old))
        setattr(target, name, value)

    def setitem(self, mapping, key, value):
        old = mapping[key] if key in mapping else _NOTSET
        self._undo.append((mapping, key, old, True))
        mapping[key] = value

    def undo(self):
        while self._undo:
            entry = self._undo.pop()
            if isinstance(entry, _Chdir):
                os.chdir(entry.old)
            elif len(entry) == 4:
                mapping, key, old, _ = entry
                if old is _NOTSET:
                    mapping.pop(key, None)
                else:
                    mapping[key] = old
            else:
                obj, name, old = entry
                if old is _NOTSET:
                    delattr(obj, name)
                else:
                    setattr(obj, name, old)


class _Raises:
    def __init__(self, expected, match=None):
        self.expected, self.match, self.value = expected, match, None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            raise AssertionError(f"Expected {getattr(self.expected, '__name__', self.expected)} to be raised, but nothing was.")
        if not issubclass(exc_type, self.expected):
            return False
        if self.match is not None and not re.search(self.match, str(exc)):
            raise AssertionError(f"The error message {str(exc)!r} did not match {self.match!r}.")
        self.value = exc
        return True


class _Approx:
    def __init__(self, expected, rel=None, abs=None):
        self.expected = expected
        self.rel = 1e-6 if rel is None else rel
        self.abs = 1e-12 if abs is None else abs

    def __eq__(self, actual):
        tolerance = max(self.rel * builtins.abs(self.expected), self.abs)
        return builtins.abs(actual - self.expected) <= tolerance

    def __repr__(self):
        return f"{self.expected} ± {max(self.rel * builtins.abs(self.expected), self.abs):.1e}"


def _fail(reason=""):
    raise AssertionError(reason or "Failed.")


def _make_pytest_module():
    module = types.ModuleType("pytest")
    module.raises = _Raises
    module.approx = _Approx
    module.fail = _fail
    return module


@contextlib.contextmanager
def _fake_pytest():
    previous = sys.modules.get("pytest")
    sys.modules["pytest"] = _make_pytest_module()
    try:
        yield
    finally:
        if previous is None:
            sys.modules.pop("pytest", None)
        else:
            sys.modules["pytest"] = previous


class _ExerciseFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Makes ``import exercise`` run the learner's code."""

    def __init__(self, source):
        self._source = source

    def find_spec(self, fullname, path=None, target=None):
        if fullname == "exercise":
            return importlib.util.spec_from_loader(fullname, self)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        module.__dict__["__file__"] = EXERCISE_FILE
        exec(compile(self._source, EXERCISE_FILE, "exec", dont_inherit=True), module.__dict__)


def _build_fixtures(func, available, tmp_dirs):
    kwargs = {}
    for name in inspect.signature(func).parameters:
        if name == "tmp_path":
            folder = tempfile.mkdtemp(prefix="learn-python-")
            tmp_dirs.append(folder)
            kwargs[name] = pathlib.Path(folder)
        elif name not in available:
            raise _UnsupportedFixture(
                f"This lesson's check uses the pytest fixture {name!r}, which the browser "
                "runner does not support yet. Please report this lesson."
            )
        else:
            kwargs[name] = available[name]
    return kwargs


def _run_one(name, func, source):
    out, err = _BoundedBuffer(), _BoundedBuffer()
    monkeypatch = _MonkeyPatch()
    tmp_dirs = []
    finder = _ExerciseFinder(source)
    sys.modules.pop("exercise", None)
    sys.meta_path.insert(0, finder)
    importlib.invalidate_caches()
    passed, message = True, ""
    try:
        with _sandbox([], out, err):
            try:
                kwargs = _build_fixtures(func, {"capsys": _Capsys(out, err), "monkeypatch": monkeypatch}, tmp_dirs)
                func(**kwargs)
            except BaseException as exc:  # noqa: BLE001
                passed, message = False, _explain_test_failure(exc)
            finally:
                monkeypatch.undo()  # must happen inside the sandbox so input() is restored properly
                for folder in tmp_dirs:
                    shutil.rmtree(folder, ignore_errors=True)
    finally:
        sys.meta_path.remove(finder)
        sys.modules.pop("exercise", None)
    return {"name": name, "passed": passed, "message": message}


def run_tests(source, tests_source):
    _register_source(source)
    namespace = {"__name__": "test_exercise"}
    with _fake_pytest():
        try:
            exec(compile(tests_source, TEST_FILE, "exec", dont_inherit=True), namespace)
        except BaseException as exc:  # noqa: BLE001
            broken = {
                "name": "(loading checks)",
                "passed": False,
                "message": "This lesson's checks could not be loaded. Please report it.\n" + _format_error(exc),
            }
            return json.dumps([broken])
        tests = [(n, f) for n, f in namespace.items() if n.startswith("test_") and callable(f)]
        return json.dumps([_run_one(n, f, source) for n, f in tests])
