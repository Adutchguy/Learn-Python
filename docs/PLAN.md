# Learn-Python — Project Plan

**Goal:** a free, open-source way for anyone to fully learn Python as effectively and quickly as possible, with no cost and no account.

**Status:** M0 (scaffold) and M1 (engine + 3 sample lessons) are built. Next: M2 (modules 0-2 and the placement test).

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

1. **Landing choice:** "I'm new to programming" / "I know another language" / "Test me".
2. **Diagnostic (~15–20 min, adaptive):** short multiple-choice, "what does this print?", and 3–4 tiny coding tasks. Questions are tagged by concept.
3. **Result:** a recommended starting module and a personalised map (skipped / review / learn). Always overridable.
4. **Fast-track for programmers:** "Python for people who already code" — compact lessons mapping familiar concepts (types, scope, loops, classes, errors) to Python idioms, then it joins the main path at Functions/Data Structures.
5. **Module checkpoints:** passing a short checkpoint test marks a whole module as done.

## 4. Curriculum (core ≈ 66 lessons + 4 projects)

| # | Module | Key topics | Project |
|---|---|---|---|
| 0 | Start Here | How this works, running code, reading error messages | — |
| 1 | Foundations (8) | Values & types, variables, operators, input/print, strings basics, f-strings, numbers, booleans | — |
| 2 | Control Flow (6) | `if/elif/else`, `while`, `for`, `range`, `break/continue`, nested logic | Number-guessing game |
| 3 | Data Structures (8) | Lists, tuples, dicts, sets, slicing, sorting, comprehensions, choosing the right structure | — |
| 4 | Functions (7) | Defining, params/args/kwargs, return, scope, lambdas, recursion, docstrings & type hints | Text-adventure / quiz engine |
| 5 | Text & Files (6) | String methods, file I/O, `pathlib`, CSV, JSON, regex basics | — |
| 6 | Errors & Debugging (5) | Exceptions, `try/except`, raising, debugging strategies, `logging`, context managers | Expense-tracker CLI |
| 7 | Modules & Tooling (6) | Imports, stdlib tour (`collections`, `itertools`, `datetime`, `random`), venvs, `pip`, project layout | — |
| 8 | OOP (8) | Classes, methods, dunder methods, inheritance, composition, `dataclasses`, properties, protocols/ABCs | Inventory or bank-account system |
| 9 | Pythonic Python (7) | Iterators, generators, decorators, comprehension patterns, typing, `functools`, async intro | — |
| 10 | Testing & Quality (5) | `pytest`, fixtures, `ruff`/formatting, Git basics, packaging a small project | Capstone: build + test + publish a mini-package |

**Optional tracks (after Module 6 or 8):**
- **Data analysis:** NumPy, pandas, Matplotlib, cleaning data, a small analysis project (browser-capable).
- **Web & APIs:** HTTP concepts, `requests`, JSON APIs, a small FastAPI service (mostly local-only).
- **Automation & scripting:** files/folders, `argparse`, `subprocess`, scheduling, small tools (mostly local-only).

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
| **M4 Robust code** | Modules 6–8 + `learn` CLI + project 2–3 |
| **M5 Advanced + capstone** | Modules 9–10 + capstone + programmers' fast-track |
| **M6 Tracks & polish** | Optional tracks, accessibility pass, mobile layout, offline PWA, contributor onboarding |

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
- Lesson tests use real pytest locally and a small compatible runner in the browser (`capsys`, `monkeypatch`, `pytest.raises/approx/fail`); this subset is documented in `docs/CONTENT-STYLE-GUIDE.md`.

## 8. Risks & mitigations

- **Content volume is the real cost** (66+ lessons with tests). → Ship vertical slices per module; CI keeps quality consistent.
- **Browser Python limits** → local-only tags + graceful messaging.
- **Wrong or outdated content** → every exercise is machine-verified in CI; version-sensitive claims are checked against current docs when written.
- **Scope creep** → tracks are optional and come after the core path is solid.
