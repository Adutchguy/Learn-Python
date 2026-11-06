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


def start_repo(repo):
    repo = Path(repo)
    repo.mkdir(parents=True, exist_ok=True)
    run_git(repo, "init")
    run_git(repo, "config", "user.name", "Learner")
    run_git(repo, "config", "user.email", "learner@example.com")


def commit_file(repo, filename, text, message):
    Path(repo, filename).write_text(text, encoding="utf-8")
    run_git(repo, "add", filename)
    run_git(repo, "commit", "-m", message)


def history(repo):
    try:
        output = run_git(repo, "log", "--format=%s")
    except subprocess.CalledProcessError:
        return []
    return output.splitlines()


def uncommitted(repo):
    lines = run_git(repo, "status", "--porcelain").splitlines()
    return sorted(line[3:] for line in lines)
