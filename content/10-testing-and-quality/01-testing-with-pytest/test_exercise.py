def _reference(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return "-".join(text.lower().split())


def _forgets_lowercase(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return "-".join(text.split())


def _bad_edges(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text.lower().replace(" ", "-")


def _bad_inner_spaces(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return "-".join(text.lower().strip().split(" "))


def _accepts_anything(text):
    return "-".join(str(text).lower().split())


def _learner_tests():
    import exercise

    tests = {
        name: func
        for name, func in vars(exercise).items()
        if name.startswith("test_") and callable(func)
    }
    return exercise, tests


def _failing(exercise, tests, version):
    """Names of the learner's tests that fail when slugify is replaced by `version`."""
    original = exercise.slugify
    exercise.slugify = version
    failed = []
    try:
        for name, func in tests.items():
            try:
                func()
            except (KeyboardInterrupt, SystemExit):
                raise
            except BaseException:
                failed.append(name)
    finally:
        exercise.slugify = original
    return failed


def test_you_wrote_at_least_four_tests():
    _, tests = _learner_tests()
    assert len(tests) >= 4, f"Write at least 4 functions whose names start with test_ (found {len(tests)})."


def test_your_tests_pass_on_the_correct_function():
    exercise, tests = _learner_tests()
    assert tests, "Write some test_ functions first."
    failed = _failing(exercise, tests, _reference)
    assert not failed, f"These tests of yours fail even on a correct slugify, so they expect the wrong thing: {failed}"


def test_your_tests_notice_missing_lowercase():
    exercise, tests = _learner_tests()
    assert tests, "Write some test_ functions first."
    assert _failing(exercise, tests, _forgets_lowercase), "Your tests did not notice a slugify that forgets to lowercase. Add a test using capital letters."


def test_your_tests_notice_bad_edges():
    exercise, tests = _learner_tests()
    assert tests, "Write some test_ functions first."
    assert _failing(exercise, tests, _bad_edges), "Your tests did not notice a slugify that keeps spaces at the start or end. Add a test with leading or trailing spaces."


def test_your_tests_notice_repeated_spaces():
    exercise, tests = _learner_tests()
    assert tests, "Write some test_ functions first."
    assert _failing(exercise, tests, _bad_inner_spaces), "Your tests did not notice a slugify that turns several spaces into several hyphens. Add a test with more than one space between words."


def test_your_tests_notice_wrong_input_types():
    exercise, tests = _learner_tests()
    assert tests, "Write some test_ functions first."
    assert _failing(exercise, tests, _accepts_anything), "Your tests did not notice a slugify that accepts non-text input. Add a test using pytest.raises(TypeError)."
