QUESTIONS = [
    ("What is the capital of France?", "Paris"),
    ("What is 2 + 2?", "4"),
    ("What colour is a clear sky?", "blue"),
]


def check_answer(given, correct):
    """Return True if the answers match, ignoring spaces and capital letters."""
    # TODO
    pass


def run_quiz(questions):
    """Ask every question, print Correct! or Wrong! The answer was X, and return the score."""
    # TODO
    pass


def grade(score, total):
    """Return 'Great job!' (all right), 'Good effort!' (half or more) or 'Keep practising!'."""
    # TODO
    pass


# ---- main program: leave this as it is ----
score = run_quiz(QUESTIONS)
print(f"Score: {score}/{len(QUESTIONS)}")
print(grade(score, len(QUESTIONS)))
