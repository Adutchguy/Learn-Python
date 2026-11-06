import os
from contextlib import contextmanager


def copy_text(src, dst):
    with open(src) as source, open(dst, "w") as target:
        target.write(source.read())


@contextmanager
def working_in(path):
    original = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original)


@contextmanager
def log_block(name, lines):
    lines.append(f"start {name}")
    try:
        yield
    finally:
        lines.append(f"end {name}")
