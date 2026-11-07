# Learn-Python — Project Plan

**Goal:** a free, open-source way for anyone to fully learn Python as effectively and quickly as possible, with no cost and no account.

**Status:** M0 (scaffold), M1 (engine), M2 (modules 0-2, placement test v1, first project), M3 (modules 3-5 and the spaced-review queue), M4 (modules 6-8, the `learn` CLI, two more projects), M5 (modules 9-10, the capstone and the programmers' fast-track) and M6 (three optional tracks, accessibility pass, mobile layout, offline PWA, contributor onboarding) are built: 72 core lessons plus 16 in optional tracks. Next: the human review pass, a first public release, and whatever learners ask for.

**Decisions so far (from kickoff):**
- Delivery: **both** a no-install browser app **and** a clone-and-run repo track
- Audience: **both** complete beginners and programmers new to Python, routed by a **placement path**
- Scope: **core Python through OOP + projects**, plus **optional practical tracks** (data, web/APIs, automation)
- Process: plan first, then build

---

## 1. Design principles (what makes it fast *and* effective)

1. **Write code in the first 2 minutes.** Every lesson is short (10–15 min): a tiny explanation, a worked example, then an exercise.
2. **Active over passive.** Learners run and fix code far more than they read. Exercises have instant, specific feedback.
3. **Worked example → partly-filled → from scratch.** Early lessons use fill-in-the-blank and reorder-the-lines (Parsons) problems before blank-page problems.
4. **Spaced retrieval.** A daily "review queue" resurfaces old concepts with quick questions (simple Leitner boxes, stored locally).
5. **Interleaving.** Module quizzes mix old and new topics rather than testing only the latest lesson.
6. **Error literacy early.** A dedicated early lesson on reading tracebacks; every exercise gives hints, not just "wrong".
7. **Projects every few modules**, so skills are used together, not just in isolation.
8. **Skip what you know.** Placement test + per-module checkpoint tests let experienced learners jump ahead.
9. **Privacy-first and free.** No accounts, no tracking, progress in the browser (exportable as a file).

## 2. One source of truth for both tracks

The same lesson content feeds the web app *and* the local repo track, so they never drift apart.

```
Learn-Python/
├── content/                  # SOURCE OF TRUTH (Markdown + exercise files)
│   ├── 00-start/
│   ├── 01-foundations/
│   │   ├── 01-hello-world/
│   │   │   ├── lesson.md         # frontmatter: title, time, prereqs, concepts, track flags
│   │   │   ├── starter.py        # what the learner sees
│   │   │   ├── solution.py       # reference answer (never shipped to the learner UI by default)
│   │   │   └── test_exercise.py  # pytest-compatible tests
│   │   └── ...
│   └── placement/            # diagnostic question bank
├── web/                      # static site (browser track)
├── exercises/                # GENERATED local track (starter + tests per lesson) — built by tools/
├── tools/                    # Python build/validation scripts
├── .github/workflows/        # CI + GitHub Pages deploy
├── docs/                     # this plan, contributor guide, content style guide
└── README.md
```

**Browser track**
- Static site, hosted free on GitHub Pages.
- Python runs **in the browser via Pyodide** inside a Web Worker (UI never freezes; infinite loops can be stopped).
- Code editor: CodeMirror 6.
- Site framework (recommended): **Astro** (Markdown lessons as content collections) with a small interactive island for the editor. Alternative: plain Vite + TypeScript. I'll confirm current versions of Astro, Pyodide and CodeMirror at build time rather than assume them.
- Progress, streaks and the review queue live in `localStorage`, with export/import of a progress file.
- Installable/offline-capable (PWA) once the content is stable.

**Local track**
- `tools/` generates `exercises/<module>/<lesson>/` with `starter.py` + `test_exercise.py` from `content/`.
- Learner flow: clone → `pip install -r requirements.txt` → edit file → `pytest exercises/01-foundations/01-hello-world`.
- A small `learn` CLI (`python -m learn next | check | hint`) tells you what to do next and runs the right tests, so you don't need to know pytest to start.

**Shared test format**
- Tests are plain `test_*` functions with ordinary `assert`s and a helpful message. pytest runs them locally; a tiny runner (~50 lines) runs the same functions in the browser, so no pytest in the browser is needed.

**CI (the quality gate)**
- Every `solution.py` must pass its `test_exercise.py`; every `starter.py` must *fail* (so exercises can't be accidentally pre-solved).
- Link checking, frontmatter validation (prereqs exist, no circular dependencies), build site, deploy on merge to `main`.

**Known browser limits (so we design around them)**
- No real sockets/subprocess/threads; `input()` is shimmed; network access is restricted. Lessons that need these (HTTP servers, `subprocess`, scheduling) are tagged **local-only** and appear in the repo track with a badge in the web app.
- Pandas, NumPy and Matplotlib are available in Pyodide, so the data track can run fully in the browser.

## 3. Placement path

> **Built (M2, v1):** a "what does this print?" quiz at `/placement/` with 49 multiple-choice questions in course order (47 on published lessons, 2 beyond them: `argparse` flags and thread pools). It stops after two misses, recommends the lesson of the first miss, and can mark earlier lessons as skipped (`placedOut` in progress; the orientation lesson is never skipped). Every answer key is verified by running the code in CI (`tools/placement.py`). Still to do from the list below: the landing choice, tiny coding tasks, and per-module checkpoints. The programmers' fast-track was added in M5 (item 4).

1. **Landing choice:** "I'm new to programming" / "I know another language" / "Test me".
2. **Diagnostic (~15–20 min, adaptive):** short multiple-choice, "what does this print?", and 3–4 tiny coding tasks. Questions are tagged by concept.
3. **Result:** a recommended starting module and a personalised map (skipped / review / learn). Always overridable.
4. **Fast-track for programmers (built, M5):** a page at `/fast-track/` with 18 "what is different in Python" rows (each with a short example whose output CI verifies by running it) and one button that marks the 20 lessons a programmer can skip (`content/fast-track/path.json`, reusing the `placedOut` mechanism; the orientation lesson is never skipped). Chosen over writing separate compact lessons so there is one set of lessons to maintain.
5. **Module checkpoints:** passing a short checkpoint test marks a whole module as done.

> **Review queue built (M3, extended in M4):** `content/review/questions.json` (79 questions now) holds one or two "what does this print?" questions per lesson (projects and the orientation lesson are exempt; CI checks the coverage and runs every answer key). `/review/` asks the questions from lessons the learner really completed (not ones skipped by the placement test) on a Leitner schedule: a right answer moves a question up a box (gaps of 1, 3, 7, 14, then 30 days), a wrong or "not sure" answer sends it back to box 0 (tomorrow). Sessions are capped at 10 questions. The schedule lives in the same browser progress as everything else and is included in the backup file. Still to do from principle 5: interleaved module quizzes, and a typed-code review task.

## 4. Curriculum (core: 72 lessons, including 5 projects; plus 16 in optional tracks)

| # | Module | Key topics | Project |
|---|---|---|---|
| 0 | Start Here | How this works, running code | — |
| 1 | Foundations (9) | Hello world, variables, reading error messages, types, input & conversion, arithmetic, strings, f-strings, booleans & comparisons | — |
| 2 | Control Flow (6) | `if/elif/else`, `while`, `for`, `range`, `break/continue`, nested logic | Number-guessing game |
| 3 | Data Structures (8) | Lists, looping, slicing, sorting, tuples & unpacking, dicts, sets & choosing the right structure, comprehensions | — |
| 4 | Functions (8) | Defining, return, defaults/args/kwargs, scope & mutation, lambdas, recursion, docstrings & type hints | Quiz engine |
| 5 | Text & Files (6) | String methods, file I/O, `pathlib`, CSV, JSON, regex basics | — |
| 6 | Errors & Debugging (6) | Exceptions, `try/except`, raising, debugging strategies, `logging`, context managers, then the expense tracker | Expense tracker (built) |
| 7 | Modules & Tooling (6, one terminal-only) | Imports, stdlib tour (`collections`, `itertools`, `datetime`, `random`), venvs, `pip`, project layout | — |
| 8 | OOP (9) | Classes, methods, dunder methods, inheritance, composition, `dataclasses`, properties, protocols/ABCs | Bank-account system (built) |
| 9 | Pythonic Python (7, one local-only) | Iterators, generators, comprehension patterns, decorators, `functools`, type hints, async intro | — |
| 10 | Testing & Quality (6, three local-only) | `pytest` (write tests that catch mutants), fixtures & parametrize, readable code & linting, Git basics, packaging, then the `wordkit` capstone | Capstone: build + test + publish a mini-package (built) |

**Optional tracks (built; not part of the core path, placement test or fast track):**
- **Module 11, Data Analysis (7, one local-only):** NumPy arrays, pandas DataFrames, selecting and filtering, grouping and summarising, cleaning messy data, a sales-analysis project, then Matplotlib (local-only, because a saved chart cannot be seen in the browser runner). NumPy and pandas run in the browser through Pyodide.
- **Module 12, Automation and Scripting (5, one local-only):** `argparse`, files and folders in bulk, `subprocess` (local-only), timing, retries and scheduling, and a file-organiser project.
- **Module 13, Web and APIs (4, two local-only):** how HTTP works, JSON APIs, calling a web service with `urllib` (local-only), and a tiny JSON API built on the standard library's `http.server` (local-only).

Deviation from the original idea: the web track uses the standard library (`urllib`, `http.server`) instead of `requests` and FastAPI, so it needs no extra installs and its tests can run a real server on `127.0.0.1` without touching the internet.

## 5. Lesson template (every lesson follows it)

1. **Hook** (1–2 sentences: why this matters)
2. **Concept** (≤ 150 words + one worked example)
3. **Try it** (editable, runnable code; predict the output first)
4. **Exercise** (graded; hints unlock in 3 steps; solution available after attempts)
5. **Check** (1–3 quick questions that feed the review queue)
6. **Recap + "common mistakes"**

## 6. Milestones

| Milestone | Deliverable |
|---|---|
| **M0 Scaffold** | Repo structure, README, license, contributing guide, CI skeleton, GitHub Pages deploy |
| **M1 Engine** | Web app with editor + Pyodide worker + test runner + progress; 3 sample lessons; `tools/` generates local exercises; CI checks solutions |
| **M2 Beginner core** | Modules 0–2 complete + placement test v1 + first project |
| **M3 Data & functions** | Modules 3–5 + review queue (spaced retrieval) |
| **M4 Robust code** (built) | Modules 6–8 + `learn` CLI + projects 3–4 |
| **M5 Advanced + capstone** (built) | Modules 9–10 + capstone + programmers' fast-track |
| **M6 Tracks & polish** (built) | Optional tracks, accessibility pass, mobile layout, offline PWA, contributor onboarding |

Suggested first build session: **M0 + M1** (working end-to-end vertical slice with 3 real lessons), so we can feel the learning experience before writing the remaining content.

## 7. Decisions

Resolved (all recommendations accepted):

1. **Licensing:** MIT for code, CC BY-SA 4.0 for lesson content.
2. **Site framework:** Astro.
3. **Python floor for the local track:** 3.11+.
4. **Branding/URL:** "Learn-Python" at `adutchguy.github.io/Learn-Python`.
5. **Content review:** Claude drafts every lesson; each is machine-verified in CI and spot-checked for accuracy and tone by a human reviewer. Cadence still to be chosen per module.

Findings from building M1:

- Current Pyodide releases do not support classic web workers, so the browser worker is a module worker that loads `pyodide.mjs`.
- A compile detail that mattered: the browser runner must compile learner and test code with `dont_inherit=True`, otherwise the runner's own `from __future__ import annotations` silently turns learners' type hints into strings.
- Lesson tests use real pytest locally and a small compatible runner in the browser (`capsys`, `monkeypatch` incl. `chdir`, `tmp_path`, `pytest.raises/approx/fail`); this subset is documented in `docs/CONTENT-STYLE-GUIDE.md`.

Findings from building M6:

- Optional tracks reuse the module and lesson machinery with one flag (`"optional": true` in `module.json`). Core lessons may not require track lessons; the placement test and fast track only ever see core lessons (a first draft let a perfect placement score "skip" track lessons, caught by the end-to-end test).
- Lessons declare third-party packages in `packages:` frontmatter (`numpy`, `pandas`, `matplotlib`). The browser worker preloads them with `pyodide.loadPackage` and now checks that they really loaded, because Pyodide only logs a failed download.
- An automated axe-core audit of the built site found real problems the eye missed: low-contrast code colours (fixed with high-contrast Shiki themes and an own accessible dark editor theme) and a scrollable editor region that keyboards could not reach (the editor now wraps lines).
- The service worker needs `ignoreVary` when matching its cache, because module scripts are requested with an `Origin` header and the static host answers `Vary: Origin`.
- Offline support is two layers: the site is precached by the build (an Astro integration writes the file list), and Python itself is cached from the CDN either on first use or all at once by the "Download for offline" button.

## 8. Risks & mitigations

- **Content volume is the real cost** (66+ lessons with tests). → Ship vertical slices per module; CI keeps quality consistent.
- **Browser Python limits** → local-only tags + graceful messaging.
- **Wrong or outdated content** → every exercise is machine-verified in CI; version-sensitive claims are checked against current docs when written.
- **Scope creep** → tracks are optional and come after the core path is solid.
