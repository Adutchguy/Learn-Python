QUESTIONS = [
    ("What is the capital of France?", "Paris"),
    ("What is 2 + 2?", "4"),
    ("What colour is a clear sky?", "blue"),
]


def check_answer(given, correct):
    """Return True if the answers match, ignoring spaces and capital letters."""
    return given.strip().lower() == correct.strip().lower()


def run_quiz(questions):
    """Ask every question, print Correct! or Wrong! The answer was X, and return the score."""
    score = 0
    for question, correct in questions:
        given = input(question + " ")
        if check_answer(given, correct):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The answer was {correct}")
    return score


def grade(score, total):
    """Return 'Great job!' (all right), 'Good effort!' (half or more) or 'Keep practising!'."""
    if score == total:
        return "Great job!"
    if score * 2 >= total:
        return "Good effort!"
    return "Keep practising!"


# ---- main program: leave this as it is ----
score = run_quiz(QUESTIONS)
print(f"Score: {score}/{len(QUESTIONS)}")
print(grade(score, len(QUESTIONS)))
