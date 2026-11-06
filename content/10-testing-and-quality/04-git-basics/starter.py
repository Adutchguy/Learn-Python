import subprocess
from pathlib import Path


def run_git(repo, *args):
    """Run a git command inside `repo` and return what it printed."""
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.rstrip("\n")


# Write these functions using run_git:
#   start_repo(repo)
#   commit_file(repo, filename, text, message)
#   history(repo)         -> commit messages, newest first ([] if none)
#   uncommitted(repo)     -> sorted names of files not yet committed
