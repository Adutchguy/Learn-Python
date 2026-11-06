def _load(monkeypatch, typed=()):
    """Import the learner's program with `typed` answers queued; return (module, printed text)."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            return ""

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise

    return exercise


def test_check_answer_ignores_case_and_spaces(monkeypatch):
    exercise = _load(monkeypatch)
    check = exercise.check_answer
    assert check("paris", "Paris") is True, "check_answer('paris', 'Paris') should be True: capital letters do not matter."
    assert check("  4 ", "4") is True, "check_answer('  4 ', '4') should be True: extra spaces do not matter."
    assert check("PARIS", " paris") is True, "check_answer('PARIS', ' paris') should be True."


def test_check_answer_rejects_wrong_answers(monkeypatch):
    exercise = _load(monkeypatch)
    result = exercise.check_answer("london", "Paris")
    assert result is False, f"check_answer('london', 'Paris') should be False but returned {result!r}."


def test_run_quiz_returns_the_score(monkeypatch):
    exercise = _load(monkeypatch)
    answers = iter(["x", "y", "z"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    score = exercise.run_quiz([("q1?", "x"), ("q2?", "nope"), ("q3?", "z")])
    assert score == 2, f"run_quiz should return the number of correct answers (2 here) but returned {score!r}."


def test_run_quiz_prints_feedback(monkeypatch, capsys):
    exercise = _load(monkeypatch)
    capsys.readouterr()
    answers = iter(["x", "wrong"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    exercise.run_quiz([("q1?", "x"), ("q2?", "right")])
    out = capsys.readouterr().out
    assert out == "Correct!\nWrong! The answer was right\n", f"run_quiz should print 'Correct!' then 'Wrong! The answer was right' but printed {out!r}."


def test_run_quiz_asks_with_the_question_text(monkeypatch):
    exercise = _load(monkeypatch)
    prompts = []

    def spy(prompt=""):
        prompts.append(prompt)
        return ""

    monkeypatch.setattr("builtins.input", spy)
    exercise.run_quiz([("Name?", "a")])
    assert prompts == ["Name? "], f"run_quiz should call input(question + ' ') so the prompt is 'Name? ' but it was {prompts!r}."


def test_grade_messages(monkeypatch):
    exercise = _load(monkeypatch)
    grade = exercise.grade
    assert grade(3, 3) == "Great job!", f"grade(3, 3) should be 'Great job!' but was {grade(3, 3)!r}."
    assert grade(2, 3) == "Good effort!", f"grade(2, 3) should be 'Good effort!' but was {grade(2, 3)!r}."
    assert grade(2, 4) == "Good effort!", f"grade(2, 4) (exactly half) should be 'Good effort!' but was {grade(2, 4)!r}."
    assert grade(1, 3) == "Keep practising!", f"grade(1, 3) should be 'Keep practising!' but was {grade(1, 3)!r}."
    assert grade(0, 3) == "Keep practising!", f"grade(0, 3) should be 'Keep practising!' but was {grade(0, 3)!r}."


def test_whole_program_with_a_good_run(monkeypatch, capsys):
    _load(monkeypatch, ["paris", " 4 ", "green"])
    out = capsys.readouterr().out.strip()
    want = "Correct!\nCorrect!\nWrong! The answer was blue\nScore: 2/3\nGood effort!"
    assert out == want, f"With the answers paris, ' 4 ' and green the program should print:\n{want}\n\nbut it printed:\n{out}"


def test_whole_program_with_a_perfect_run(monkeypatch, capsys):
    _load(monkeypatch, ["PARIS", "4", "Blue"])
    out = capsys.readouterr().out.strip()
    want = "Correct!\nCorrect!\nCorrect!\nScore: 3/3\nGreat job!"
    assert out == want, f"With three right answers the program should print:\n{want}\n\nbut it printed:\n{out}"
