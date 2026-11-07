# Contributing

Thanks for helping people learn Python! The goal is lessons that are **short, correct, kind to beginners and machine-verified**. You do not need to be an expert: fixing a confusing sentence is as welcome as writing a lesson.

## Ways to help

- **Report a problem.** Confusing wording, a wrong explanation or a check that rejects a correct answer all count as bugs. Open an issue and name the lesson.
- **Review a lesson.** Lessons are drafted with AI help and then checked by people. Read one as a beginner and tell us where you got stuck.
- **Write or improve a lesson.** See below.
- **Improve the site.** Accessibility, mobile layout and offline use matter here. See [Working on the website](#working-on-the-website).

Look for issues labelled `good first issue`.

## Get set up

You need Python 3.11+ and, for the website, Node 22+.

```bash
git clone https://github.com/Adutchguy/Learn-Python.git
cd Learn-Python
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-tracks.txt
cd web && npm ci && cd ..
```

Confirm everything works before you change anything:

```bash
python tools/validate_content.py && python tools/check_solutions.py
```

## How the repository fits together

| Folder | What it is | Edit it? |
| --- | --- | --- |
| `content/` | Every lesson, plus placement, review and fast-track questions. **The single source of truth.** | Yes |
| `exercises/` | The "work on your own computer" track, generated from `content/`. | No, run `python tools/build_exercises.py` |
| `web/` | The website (Astro). It reads `content/` directly and runs Python in the browser with Pyodide. | For site changes |
| `learn/` | The small `python -m learn` command-line helper for the local track. | For CLI changes |
| `tools/` | Validators, generators and the new-lesson scaffold. | For tooling changes |
| `docs/` | The plan and the [content style guide](docs/CONTENT-STYLE-GUIDE.md). | Yes |

## Ground rules

1. **`content/` is the only place lessons are edited.** `exercises/` is generated.
2. **Every exercise is machine-checked in CI.** The solution must pass its tests and the starter must fail them.
3. **Every `assert` in a lesson test carries a helpful message** that tells the learner what to do, not just that they were wrong. CI enforces this.
4. Follow the [content style guide](docs/CONTENT-STYLE-GUIDE.md) for tone, structure and what the browser runner supports.
5. Claims about current versions, tools or prices should be checked against official sources when written.

## Adding a lesson

Let the scaffold create the files and numbering for you:

```bash
python tools/new_lesson.py "Sets and frozensets" --module 03-data-structures
```

It creates `content/03-data-structures/NN-sets-and-frozensets/` with `lesson.md`, `starter.py`, `solution.py` and `test_exercise.py`, and sets the prerequisite to the previous lesson. Useful options:

| Option | When to use it |
| --- | --- |
| `--minutes N` | The lesson takes about N minutes (1 to 60). |
| `--local-only` | It needs real network, subprocesses or threads, so it cannot run in a browser. |
| `--packages numpy pandas` | It needs a third-party package (`numpy`, `pandas` or `matplotlib`). |
| `--new-module "Title"` | Start a new module. Add `--optional` to make it an optional track. |

Then:

1. Replace every placeholder. The validator refuses lessons that still contain the `SCAFFOLD` line, so an unfinished lesson cannot be merged by accident.
2. Add one or two questions for the lesson to `content/review/questions.json` (see the style guide). You do not work out the answer key by hand: the validator runs each program and tells you the right answer.
3. Run the checks:

   ```bash
   python tools/validate_content.py
   python tools/build_exercises.py
   python tools/check_solutions.py
   python -m pytest tools/tests
   cd web && npm test
   ```

4. Read your lesson in the browser as a beginner would: `cd web && npm run dev`.
5. Commit **both** `content/` and the regenerated `exercises/` files.

### Optional tracks

Data Analysis, Automation and Web & APIs are **optional tracks**: modules whose `module.json` has `"optional": true`. They are not part of the core path, the placement test or the fast track. A core lesson may never require an optional lesson (the validator checks), but a track lesson may build on core lessons. Track lessons that use `numpy`, `pandas` or `matplotlib` declare them in `packages:`. In the browser they are downloaded on first use; locally they come from `requirements-tracks.txt`.

## Working on the website

```bash
cd web
npm run dev        # live preview
npm run build      # production build, including the offline service worker
```

Please keep these in mind; they are the things a visitor on a phone, with a screen reader or without a connection relies on:

- **Accessibility.** Keep the skip link, headings and landmarks; every interactive element needs a visible focus state and a name; never rely on colour alone to show pass or fail. Code and UI colours need at least 4.5:1 contrast in both light and dark mode. Run an [axe](https://github.com/dequelabs/axe-core) audit if you change styles or markup.
- **Mobile.** The layout must work at 360 px wide with no sideways page scroll, and tap targets should be at least 44 px on touch screens.
- **Offline.** `web/public/sw.js` is a template: `web/integrations/pwa.mjs` fills in the file list when the site is built. New files in `web/public/` are picked up automatically. Test offline behaviour in a production build (`npm run build && npm run preview`), because the service worker is off in `npm run dev`.

## Pull requests

- One lesson or one fix per pull request keeps review quick.
- CI must be green. It validates content, checks `exercises/` is up to date, runs every lesson through real pytest *and* through the in-browser runner on real Pyodide, and builds the site.
- Explain *why* the lesson teaches things in this order if the ordering is not obvious.
- The pull request template has a short checklist; please tick it honestly.

## Licensing

By contributing you agree that code is released under the [MIT license](LICENSE) and lesson text under [CC BY-SA 4.0](LICENSE-CONTENT.txt).

## Reporting problems

Open an issue and include the lesson name and, if it is a checking problem, the code you wrote.
