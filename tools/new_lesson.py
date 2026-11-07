#!/usr/bin/env python3
"""Create the files for a new lesson (or a whole new module) from a template.

Examples::

    python tools/new_lesson.py "Sets and frozensets" --module 03-data-structures
    python tools/new_lesson.py "Reading a CSV" --module 11-data-analysis --packages pandas
    python tools/new_lesson.py "Talking to a server" --module 13-web-and-apis --local-only
    python tools/new_lesson.py "Plotting" --new-module "Plotting" --optional

The lesson is numbered after the last one in its module. The files it creates deliberately fail
`python tools/validate_content.py` until you replace the placeholder text (the validator looks for the
SCAFFOLD marker), so an unfinished lesson can never be merged by accident.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

from content import ALLOWED_PACKAGES, CONTENT, NON_COURSE_DIRS, SLUG_RE

SCAFFOLD_MARKER = "SCAFFOLD"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not slug:
        raise SystemExit(f"Cannot make a folder name from {text!r}. Use letters or numbers.")
    return slug


def module_dirs() -> list:
    return sorted(
        d for d in CONTENT.iterdir() if d.is_dir() and d.name not in NON_COURSE_DIRS and (d / "module.json").exists()
    )


def next_number(parent, existing) -> str:
    numbers = [int(d.name[:2]) for d in existing if SLUG_RE.match(d.name)]
    return f"{(max(numbers) + 1 if numbers else 1):02d}"


def lesson_dirs(module_dir) -> list:
    return sorted(d for d in module_dir.iterdir() if d.is_dir() and SLUG_RE.match(d.name))


def resolve_module(query: str):
    """Accept the full folder name, the number or any part of the name."""
    modules = module_dirs()
    q = query.lower().strip("/")
    exact = [m for m in modules if m.name == q or m.name[:2] == q.zfill(2)]
    matches = exact or [m for m in modules if q in m.name]
    if len(matches) != 1:
        names = ", ".join(m.name for m in modules)
        raise SystemExit(f"Which module is {query!r}? " + (f"It matches {len(matches)}. " if matches else "") + f"Choose from: {names}")
    return matches[0]


def previous_lesson_id(module_dir):
    """The lesson just before the new one: the last in this module, else the last of the module before it."""
    mine = lesson_dirs(module_dir)
    if mine:
        return f"{module_dir.name}/{mine[-1].name}"
    earlier = [m for m in module_dirs() if m.name < module_dir.name]
    for m in reversed(earlier):
        lessons = lesson_dirs(m)
        if lessons:
            return f"{m.name}/{lessons[-1].name}"
    return None


LESSON_TEMPLATE = """---
title: {title}
minutes: {minutes}
prereqs: {prereqs}
concepts: [replace-with-the-ideas-this-lesson-teaches]
local_only: {local_only}
{packages}hints:
  - "A nudge that points at the idea without giving the answer away."
  - "A more specific hint: say which tool or line to look at."
  - "The near-answer: show the shape of the solution, so the learner is never stuck."
---

<!-- {marker}: delete this line once you have replaced every placeholder below. -->

## Why this matters

One or two sentences on why a learner would want this. Start from a real situation, not a definition.

## The idea

Explain the idea in small steps, with short code examples. See docs/CONTENT-STYLE-GUIDE.md for tone and length.

## Your turn

Say exactly what the learner should do, and what the finished program should show.

## Recap

- One bullet per idea the learner should now be able to use.
"""

STARTER = """# Replace this with the code the learner starts from. Use TODO comments to say what to do.

answer = None
"""

SOLUTION = """# Replace this with a reference answer that passes every test.

answer = 42
"""

TEST = '''def test_answer_has_the_right_value():
    import exercise

    # Every assert needs a message that tells the learner what to do, not only that they were wrong.
    assert exercise.answer == 42, (
        f"answer should be 42, but it is {exercise.answer!r}. Replace this check with your own."
    )
'''


def create_module(title: str, optional: bool, description: str):
    slug = f"{next_number(CONTENT, module_dirs())}-{slugify(title)}"
    folder = CONTENT / slug
    folder.mkdir()
    meta = {"title": title, "description": description or "Replace this with one sentence about the module."}
    if optional:
        meta["optional"] = True
    (folder / "module.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Created module  content/{slug}/module.json")
    return folder


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Create a new lesson from a template.")
    parser.add_argument("title", help="the lesson title, for example 'Sets and frozensets'")
    where = parser.add_mutually_exclusive_group(required=True)
    where.add_argument("--module", help="the module to add it to (folder name, number, or part of the name)")
    where.add_argument("--new-module", metavar="TITLE", help="create a new module with this title and put the lesson in it")
    parser.add_argument("--optional", action="store_true", help="with --new-module: make it an optional track")
    parser.add_argument("--description", default="", help="with --new-module: one sentence describing the module")
    parser.add_argument("--minutes", type=int, default=15, help="how long it takes (1 to 60, default 15)")
    parser.add_argument("--local-only", action="store_true", help="the lesson cannot run in the browser (network, subprocesses...)")
    parser.add_argument("--packages", nargs="+", choices=sorted(ALLOWED_PACKAGES), help="third-party packages the lesson needs")
    args = parser.parse_args(argv)

    if args.optional and not args.new_module:
        parser.error("--optional only applies together with --new-module")
    if not 1 <= args.minutes <= 60:
        parser.error("--minutes must be between 1 and 60")

    module_dir = create_module(args.new_module, args.optional, args.description) if args.new_module else resolve_module(args.module)
    folder = module_dir / f"{next_number(module_dir, lesson_dirs(module_dir))}-{slugify(args.title)}"
    prev = previous_lesson_id(module_dir)
    folder.mkdir()

    title = json.dumps(args.title) if re.search(r"[:#\[\]{}]", args.title) else args.title
    packages = f"packages: [{', '.join(args.packages)}]\n" if args.packages else ""
    (folder / "lesson.md").write_text(
        LESSON_TEMPLATE.format(
            title=title,
            minutes=args.minutes,
            prereqs=json.dumps([prev] if prev else []),
            local_only="true" if args.local_only else "false",
            packages=packages,
            marker=SCAFFOLD_MARKER,
        ),
        encoding="utf-8",
    )
    (folder / "starter.py").write_text(STARTER, encoding="utf-8")
    (folder / "solution.py").write_text(SOLUTION, encoding="utf-8")
    (folder / "test_exercise.py").write_text(TEST, encoding="utf-8")

    lesson_id = f"{module_dir.name}/{folder.name}"
    print(f"Created lesson  content/{lesson_id}/  (lesson.md, starter.py, solution.py, test_exercise.py)")
    print(
        f"""
Next steps:
  1. Write the lesson and replace every placeholder (the validator fails until the SCAFFOLD line is gone).
  2. Add at least one question for "{lesson_id}" to content/review/questions.json.
  3. python tools/validate_content.py
     python tools/build_exercises.py
     python tools/check_solutions.py
     cd web && npm test
  4. Preview it: cd web && npm run dev
  5. Commit content/ and the regenerated exercises/ together.
"""
    )
    if args.local_only:
        print("This lesson is local-only: say in the lesson text that it runs on the learner's own computer.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
