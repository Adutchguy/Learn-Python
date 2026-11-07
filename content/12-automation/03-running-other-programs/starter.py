import subprocess
import sys


# Write four functions:
#
# def run(command): ...                    run a command (a list); return (returncode, stdout)
# def python_version(): ...                what `python --version` prints, stripped
# def run_or_none(command, timeout): ...   stripped output, or None on a timeout or a missing program
# def echo_safely(text): ...               a child Python prints its argument; return it, stripped
