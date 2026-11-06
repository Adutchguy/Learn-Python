# Learn Python

A free, open-source way to learn Python quickly and thoroughly, with **no sign-up and nothing to pay for**.

- **In your browser:** short interactive lessons with a built-in code editor. Python runs right in the page, so there is nothing to install. *(Live site: https://adutchguy.github.io/Learn-Python/ once GitHub Pages is switched on, see [Publishing](#publishing-the-website).)*
- **On your own computer:** the same lessons as ordinary Python files, checked with `pytest`.

Both tracks come from the same lesson files, so they always match.

> **Status:** early. The engine works end to end and there are 3 sample lessons. More modules are being added; see [docs/PLAN.md](docs/PLAN.md) for the full roadmap.

## How learning works here

Every lesson takes 10 to 15 minutes: a short explanation, a worked example, then an exercise that is checked automatically with plain-language feedback. Hints unlock one at a time, and the solution unlocks after a few honest attempts. The ideas behind the design (active practice, spaced review, early error-message skills, projects) are described in [docs/PLAN.md](docs/PLAN.md).

## Work on your own computer

You need Python 3.11 or newer.

```bash
git clone https://github.com/Adutchguy/Learn-Python.git
cd Learn-Python

python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Each lesson is a folder under `exercises/`:

```
exercises/01-foundations/01-hello-world/
├── LESSON.md          <- read this first
├── exercise.py        <- edit this file
└── test_exercise.py   <- the checks (read-only)
```

Check your work from the repository root:

```bash
pytest exercises/01-foundations/01-hello-world
```

Tip: work on your own branch (`git switch -c my-answers`) or in a fork, so your answers stay yours when you pull new lessons.

## Repository layout

| Folder | What it is |
|---|---|
| `content/` | **Source of truth.** One folder per lesson: `lesson.md`, `starter.py`, `solution.py`, `test_exercise.py` |
| `exercises/` | Local track, **generated** from `content/` (do not edit by hand, except `conftest.py`) |
| `web/` | The website (Astro) and the in-browser Python runner (Pyodide) |
| `tools/` | Python scripts that validate lessons and generate `exercises/` |
| `docs/` | Plan, content style guide |

## Contributing

Lessons, fixes and ideas are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [content style guide](docs/CONTENT-STYLE-GUIDE.md).

Quick start for contributors:

```bash
pip install -r requirements.txt
python tools/validate_content.py          # are all lessons well formed?
python tools/build_exercises.py           # regenerate exercises/ after editing content/
python tools/check_solutions.py           # every solution passes, every starter fails
python -m pytest tools/tests              # tests for the tooling itself

cd web
npm ci
npm test                                  # runs every lesson through the browser runner on real Pyodide
npm run dev                               # local website at http://localhost:4321/Learn-Python/
npm run build
```

Web development needs Node.js 22.23.4 or newer.

## Publishing the website

The site deploys automatically from `main` using GitHub Actions. One-time setup: in the repository on GitHub, open **Settings → Pages → Build and deployment** and set **Source** to **GitHub Actions**. The site then appears at `https://adutchguy.github.io/Learn-Python/`.

## Licenses

- Code: [MIT](LICENSE)
- Lessons and other learning content (`content/`, and the lesson files generated from it in `exercises/`): [CC BY-SA 4.0](LICENSE-CONTENT.txt)
