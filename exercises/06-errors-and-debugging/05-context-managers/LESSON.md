# Context Managers and with

*Errors and Debugging · about 18 minutes*

## Why this matters

Some things must be undone after you use them: close the file, go back to the old folder, release a lock. If an error strikes halfway, a plain "do it, then undo it" is skipped. A **context manager** guarantees the cleanup, and you already use one every time you write `with open(...)`.

## The idea

```python
with open("notes.txt") as f:
    text = f.read()
# the file is closed here, even if read() had failed
```

One `with` can manage several things: `with open(a) as x, open(b, "w") as y:`.

You can write your own with a generator-style function and `@contextmanager`. Code before `yield` is the setup, code after it is the cleanup, and `try`/`finally` makes the cleanup run even after an error:

```python
from contextlib import contextmanager

@contextmanager
def announce(name):
    print("starting", name)
    try:
        yield                    # the body of the with-block runs here
    finally:
        print("finished", name)
```

(`yield` is explained properly in Module 9. For now it just means "the with-block runs now".) Another handy one: `with contextlib.suppress(FileNotFoundError): os.remove(path)` ignores that one error.

## Try it

Use `announce("demo")` in a `with` block that prints something. Then put `1 / 0` inside the block and notice that `finished` is still printed before the error appears.

## Your turn

Write three things:

- `copy_text(src, dst)`: copy the text of the file at `src` into the file at `dst` using **one** `with` statement that opens both.
- `working_in(path)`: a context manager that changes the current directory to `path` (`os.chdir`) and **always** changes back, even if the block fails.
- `log_block(name, lines)`: a context manager that appends `"start NAME"` to the list `lines` when the block begins and `"end NAME"` when it finishes, even if the block raises an error.

## Recap

- `with` guarantees cleanup, even when an error happens.
- `@contextmanager` turns a function with one `yield` into a context manager.
- Put cleanup in `finally` so it always runs.

## Common mistakes

- **Forgetting `try`/`finally` around `yield`.** The cleanup is then skipped when the block fails.
- **Yielding twice**, which raises a `RuntimeError`.
- **Using the object after the `with` block**, for example reading from a file that is already closed (`ValueError: I/O operation on closed file`).

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/06-errors-and-debugging/05-context-managers
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

copy_text: one with statement can open two files: with open(src) as source, open(dst, "w") as target: then target.write(source.read()).

</details>

<details><summary>Hint 2</summary>

working_in: original = os.getcwd(); os.chdir(path); then try: yield and finally: os.chdir(original). Decorate the function with @contextmanager (from contextlib import contextmanager).

</details>

<details><summary>Hint 3</summary>

log_block: append f"start {name}" to lines, then try: yield and finally: append f"end {name}". The finally part runs even when the block raises an error.

</details>
