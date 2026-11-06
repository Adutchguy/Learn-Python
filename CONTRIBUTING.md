# Contributing

Thanks for helping people learn Python! The goal is lessons that are **short, correct, kind to beginners and machine-verified**.

## Ground rules

1. **`content/` is the only place lessons are edited.** `exercises/` is generated; the website reads `content/` directly.
2. **Every exercise is machine-checked in CI.** The solution must pass its tests and the starter must fail them.
3. **Every `assert` in a lesson test carries a helpful message** that tells the learner what to do, not just that they were wrong. CI enforces this.
4. Follow the [content style guide](docs/CONTENT-STYLE-GUIDE.md) for tone, structure and what the browser runner supports.
5. Claims about current versions, tools or prices should be checked against official sources when written.

## Adding a lesson

1. Pick the module folder in `content/` (or create `content/NN-name/module.json` with a `title` and `description`).
2. Create `content/<module>/NN-lesson-name/` containing:
   - `lesson.md`: YAML frontmatter plus the lesson text
   - `starter.py`: what the learner sees
   - `solution.py`: a reference answer
   - `test_exercise.py`: pytest-style checks
3. Run the checks:

   ```bash
   python tools/validate_content.py
   python tools/build_exercises.py
   python tools/check_solutions.py
   cd web && npm test
   ```

4. Preview it in the browser: `cd web && npm run dev`.
5. Commit **both** `content/` and the regenerated `exercises/` files.

## Pull requests

- One lesson or one fix per pull request keeps review quick.
- CI must be green. It validates content, checks `exercises/` is up to date, runs every lesson through real pytest *and* through the in-browser runner on real Pyodide, and builds the site.
- Explain *why* the lesson teaches things in this order if the ordering is not obvious.

## Reporting problems

Open an issue and include the lesson name and, if it is a checking problem, the code you wrote. Confusing wording counts as a bug.
