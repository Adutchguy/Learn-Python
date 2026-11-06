# Local track exercises

Each folder here is one lesson:

- `LESSON.md`: read this first
- `exercise.py`: **your** file; edit it
- `test_exercise.py`: the checks

Check one lesson from the repository root:

```bash
pytest exercises/01-foundations/01-hello-world
```

These files are **generated** from `content/` by `python tools/build_exercises.py`. Contributors should edit `content/`, not this folder. (`conftest.py` and this README are the only hand-written files here.)
