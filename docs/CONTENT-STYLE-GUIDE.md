# Content style guide

How to write lessons that teach quickly and check reliably.

## Lesson folder

```
content/<NN-module>/<NN-lesson>/
├── lesson.md
├── starter.py
├── solution.py
└── test_exercise.py
```

The quickest way to start is `python tools/new_lesson.py "Title" --module <module>`, which creates these files with the numbering and prerequisite filled in (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

Folder names are `NN-lowercase-words` (for example `03-data-structures/02-dictionaries`). The numbers set the order. A lesson id is `<module>/<lesson>`, for example `01-foundations/02-variables`.

## Frontmatter (`lesson.md`)

```yaml
---
title: Variables                     # shown to learners
minutes: 12                          # honest estimate, 1-60
prereqs: ["01-foundations/01-hello-world"]   # lesson ids that must come earlier; [] for none
concepts: [variable, assignment]     # what this lesson teaches (used later for review and placement)
local_only: false                    # true if it cannot run in a browser (see below)
hints:                               # exactly three, each a little more revealing than the last
  - "..."
  - "..."
  - "..."
---
```

Quote any frontmatter value that contains `:`, `*` or `#` (for example `concepts: ["*args"]`); the validator reports invalid YAML with a hint.

Optional keys:

- `broken_starter: true` allows a `starter.py` that does not even parse (only for lessons about fixing errors).
- `packages: [numpy, pandas]` lists the third-party packages the lesson needs. Only `numpy`, `pandas` and `matplotlib` are allowed. In the browser, Pyodide downloads them before the lesson starts (the first time takes a while, and the page says so). Locally they come from `requirements-tracks.txt`. A lesson whose output cannot be seen in the browser (for example a saved chart) should also be `local_only: true`.

Unknown keys are rejected.

## Optional tracks

A module whose `module.json` contains `"optional": true` is an **optional track** (Data Analysis, Automation & scripting, Web & APIs). Tracks are listed after the core course, are never counted in the core progress, and are left out of the placement test and the fast track. A core lesson may not list a track lesson in `prereqs`; a track lesson may build on core lessons. Give each track lesson review questions like any other lesson. Keep project lessons at the end of a track and title them `Project: ...`.

## Lesson body

Use these headings in this order (`## Your turn` and `## Recap` are required; CI checks):

1. `## Why this matters`: one to three sentences.
2. `## The idea`: at most about 150 words and one worked example.
3. `## Try it`: invite the learner to change the example and predict the result.
4. `## Your turn`: exactly what to do and what "done" looks like.
5. `## Recap`: three bullets at most.
6. `## Common mistakes`: the real errors learners hit, with the error name they will see.

### Tone

- Friendly, direct, second person ("you"). No jokes at the learner's expense.
- Introduce one idea at a time. If a line of starter code uses something not taught yet (like `int(input())`), say so and tell the learner to leave it alone.
- Show errors as normal. Name the exact error type the learner will see.
- Plain words first, jargon second (bold the term once, when it is defined).

## Exercises

- Prefer a task that takes 2 to 5 minutes and has one clear success condition.
- The **starter must fail** the tests, and the **solution must pass**. `python tools/check_solutions.py` proves both.
- Use comments in `starter.py` (`# TODO 1: ...`) to break the task into steps.
- Do not require a specific coding style when behaviour is what matters.

## Tests (`test_exercise.py`)

Tests are ordinary pytest tests, run by **real pytest** locally and by a small compatible runner in the browser.

Rules:

1. **Every `assert` has a message** that tells the learner what to do:
   ```python
   assert out == "Hello, Python!\n", f"Expected Hello, Python! but your program printed {out!r}."
   ```
2. Import the learner's code **inside the test**: `import exercise`. Each test gets a fresh import, which runs the learner's program. Do not import at the top of the file.
3. Give each behaviour its own test function with a descriptive name (`test_exactly_25_is_hot`). The learner sees these names.
4. Provide feedback a beginner can act on: show what was expected and what they got, using `!r` for strings.

### What the browser runner supports

| Supported | Notes |
|---|---|
| `test_*` functions, `assert` | |
| `capsys` fixture | `capsys.readouterr()` with `.out` / `.err` |
| `monkeypatch` fixture | `setattr("module.attr", value)`, `setattr(obj, "name", value)`, `setitem`, `chdir(path)`; undone after each test |
| `tmp_path` fixture | a fresh empty temporary folder (a `pathlib.Path`), removed after the test. Write file lessons as functions that take a path so the checks never touch the learner's own files |
| `pytest.raises`, `pytest.approx`, `pytest.fail` | `approx` handles numbers only |

Anything else (`parametrize`, `request`, plugins, ...) works locally but **not in the browser**. If a lesson needs it, either rewrite the test to avoid it or mark the lesson `local_only: true`.

### Testing `input()`

Patch it in the test with `monkeypatch.setattr("builtins.input", lambda prompt="": "30")`. In the browser, learners type values into the Input box when they press **Run**.

### Testing things that are random, on disk, or logged

- **Randomness:** make the function take a `random.Random` (for example `roll_dice(count, rng)`), and have the test pass `random.Random(42)`. Never assert on unseeded random output.
- **Files:** use `tmp_path` for anything the learner's code writes. If the code works relative to the current folder, call `monkeypatch.chdir(tmp_path)` so a failing test cannot leave files behind.
- **Logging:** give each test a fresh logger name, because loggers are global and would otherwise carry handlers from one test into the next.
- **Collaborators:** when a lesson is about composition, test with a small fake object (a duck type) instead of the learner's other class.
- **Report text:** when a result contains values that may legitimately be formatted in more than one way, check the pieces (for example `"12.50" in line`) instead of the exact whole line.

## `local_only` lessons

Browsers cannot provide real network sockets, subprocesses or threads. Lessons about those topics set `local_only: true`. When a lesson needs a server, start one inside the test on `127.0.0.1` (for example with `http.server`) rather than calling a real website, so the checks never depend on the internet or on someone else's service. They appear on the website with instructions to use the local track, and the browser-runner tests skip them. Their tests may use any pytest feature. In practice that means `parametrize`, fixtures, `skip`, `asyncio.run`, Git, packaging tools and anything else the in-browser pytest cannot do.

## Teaching testing and code quality

- **Tests-of-tests:** to teach testing, have the learner write the tests. The checker runs them against a correct reference and against deliberate mutants, and the tests must fail on every mutant (see `10-testing-and-quality/01` and the capstone).
- **Checking code style in the browser:** use `ast` plus `linecache.getlines(exercise.__file__)`. The runner registers the learner's source there, so this works in the browser and locally.
- **Each test imports `exercise` fresh:** the runner removes it from `sys.modules` between tests, so do not rely on state surviving.

## Checklist before opening a pull request

- [ ] `python tools/validate_content.py` is clean
- [ ] `python tools/build_exercises.py` has been run and its output committed
- [ ] `python tools/check_solutions.py` passes
- [ ] `cd web && npm test` passes
- [ ] A new lesson has one or two questions in `content/review/questions.json`
- [ ] You read the lesson in the browser (`npm run dev`) and it makes sense to a complete beginner

## Placement-test questions

The placement test lives in `content/placement/questions.json`. Each question is a short program and four or so options.

- Keep questions in **course order** (by the lesson they test). Questions for topics with no lesson yet use `"lesson": null` and a `"topic"`, and go last.
- Options are plain strings; use `\n` for options that print several lines. Add `"stdin"` if the program reads input. Use `"kind": "error"` when the question is "which error is this?", and list the exception name as the right option.
- Every question needs an `"explanation"` that teaches, in one or two sentences.
- You do not need to work out the answer by hand: `python tools/validate_content.py` runs each program and fails if the answer key does not match what Python really prints.

## Review questions

Each lesson (except projects and the orientation lesson) needs one or two questions in `content/review/questions.json`. They feed the spaced-review queue, so aim for *retrieval of the key idea*, not trivia:

- Same format as the placement questions, but every question needs a `lesson`; keep the file in course order.
- Prefer short programs whose output shows the idea (and the usual misconception as a wrong option). Use `"kind": "error"` for "which error is this?".
- You do not work out the answer by hand: `python tools/validate_content.py` runs the code and fails if the key is wrong. CI also fails if a lesson has no review question.

