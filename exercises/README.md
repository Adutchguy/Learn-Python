# Local track exercises

Each folder here is one lesson:

- `LESSON.md`: read this first
- `exercise.py`: **your** file; edit it
- `test_exercise.py`: the checks

From the repository root, `python -m learn` tells you which lesson is next, `python -m learn check` runs its checks and `python -m learn hint` gives a hint. You can also check one lesson directly:

```bash
pytest exercises/01-foundations/01-hello-world
```

These files are **generated** from `content/` by `python tools/build_exercises.py`. Contributors should edit `content/`, not this folder. (`conftest.py` and this README are the only hand-written files here.)
