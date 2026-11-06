"""Remember which lessons are finished, and how many hints were used (a small JSON file)."""

from __future__ import annotations

import json
import os
from pathlib import Path

FILE_NAME = ".learn-progress.json"


class Progress:
    def __init__(self, path: Path):
        self.path = path
        self.completed: set[str] = set()
        self.hints_seen: dict[str, int] = {}
        self._load()

    def _load(self) -> None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return  # missing or damaged file: start fresh rather than crash
        if not isinstance(data, dict):
            return
        completed = data.get("completed")
        if isinstance(completed, list):
            self.completed = {c for c in completed if isinstance(c, str)}
        hints = data.get("hints")
        if isinstance(hints, dict):
            self.hints_seen = {k: v for k, v in hints.items() if isinstance(k, str) and isinstance(v, int) and v >= 0}

    def save(self) -> None:
        data = {"version": 1, "completed": sorted(self.completed), "hints": dict(sorted(self.hints_seen.items()))}
        temporary = self.path.with_name(self.path.name + ".tmp")
        temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
        os.replace(temporary, self.path)
