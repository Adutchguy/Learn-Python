"""Shared pytest setup for every lesson exercise.

Each test starts with a *fresh* import of the learner's ``exercise.py`` from the
lesson's own folder, so ``import exercise`` inside a test always re-runs the
learner's program. The in-browser runner (web/public/py/learn_runner.py)
provides the same guarantee.

This file is maintained by hand; ``tools/build_exercises.py`` leaves it alone.
"""

import importlib
import sys

import pytest


@pytest.fixture(autouse=True)
def _fresh_exercise_module(request, monkeypatch):
    monkeypatch.syspath_prepend(str(request.path.parent))
    monkeypatch.setattr(sys, "dont_write_bytecode", True)
    sys.modules.pop("exercise", None)
    importlib.invalidate_caches()
    yield
    sys.modules.pop("exercise", None)
