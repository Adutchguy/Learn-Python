---
title: "Git Basics: Saving the History of Your Work"
minutes: 20
prereqs: ["10-testing-and-quality/03-readable-code-and-linting"]
concepts: ["git", "repository", "commit", "staging area", "git log", "git status", "subprocess"]
local_only: true
hints:
  - "start_repo: make the folder (repo.mkdir(parents=True, exist_ok=True)), then run_git(repo, \"init\"), then set the author for this repository with run_git(repo, \"config\", \"user.name\", \"Learner\") and the same for user.email, otherwise commits can fail."
  - "commit_file: write the file with Path(repo, filename).write_text(text), then run_git(repo, \"add\", filename) and run_git(repo, \"commit\", \"-m\", message). history: run_git(repo, \"log\", \"--format=%s\").splitlines(). A brand-new repository has no commits, and git log then fails with CalledProcessError: catch it and return []."
  - "uncommitted: run_git(repo, \"status\", \"--porcelain\") prints one line per changed file: two status characters, a space, then the file name. So the name is line[3:]. Return the names sorted."
---

## Why this matters

**Git** records the history of your project. You can go back to any earlier version, see what changed and why, try ideas safely on a branch, and work with other people without overwriting each other. Nearly every software team uses it, and your own projects deserve it too.

## The idea

Git works in a **repository** (a folder with a hidden `.git` directory). The everyday cycle is: change files, **stage** the changes you want, then **commit** them with a message.

```bash
git init                      # make this folder a repository (once)
git status                    # what changed? what is staged?
git add notes.txt             # stage a file for the next commit
git commit -m "Add notes"     # save a snapshot with a message
git log --oneline             # list the history, newest first
git diff                      # show unstaged changes line by line
```

Useful next steps:

```bash
git switch -c experiment      # create and switch to a new branch
git switch main               # go back
git merge experiment          # bring the branch's work into this one
git clone <url>               # copy a repository from the internet
git push / git pull           # send / fetch commits to / from a remote
```

Habits that pay off:

- Commit small, finished steps, with a message that says **what and why** ("Fix rounding of totals"), not "stuff".
- List files that should never be committed (`.venv/`, `__pycache__/`, secrets, big data) in a `.gitignore` file.
- Never commit passwords or API keys. Once pushed, assume they are public.

Git runs in a terminal, and programs can drive it too: Python's `subprocess` module runs a command and captures what it prints. That is what this lesson's exercise does, so it runs on your own computer and needs Git installed (`git --version`).

## Try it

In a temporary folder on your computer, run `git init`, create a file, then run the status, add, commit and log commands above, one at a time, and watch the output change.

## Your turn

The starter has a helper `run_git(repo, *args)` that runs a Git command inside a folder and returns what it prints. Using it, write:

- `start_repo(repo)`: create the folder if needed, run `git init`, and set `user.name` and `user.email` for this repository.
- `commit_file(repo, filename, text, message)`: write the file, stage it and commit it.
- `history(repo)`: the list of commit messages, newest first. A repository with no commits gives `[]`.
- `uncommitted(repo)`: the sorted names of files that are changed, staged or new and not yet committed.

## Recap

- A repository stores history; a commit is a saved snapshot with a message.
- The cycle: edit, `git add`, `git commit`; check with `git status` and `git log`.
- Branches let you experiment safely; `.gitignore` keeps junk out.
- `subprocess.run` lets Python drive command-line tools.

## Common mistakes

- **Forgetting to stage** (`git add`) so the commit is empty.
- **Committing secrets or generated files.**
- **Vague messages** like "update", which make the history useless.
