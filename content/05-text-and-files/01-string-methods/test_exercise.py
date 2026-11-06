def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_clean_name():
    result = _fn("clean_name")("  aDA   LOVElace ")
    assert result == "Ada Lovelace", f"clean_name('  aDA   LOVElace ') should return 'Ada Lovelace' but returned {result!r}."


def test_clean_name_single_word():
    result = _fn("clean_name")("  ZED")
    assert result == "Zed", f"clean_name('  ZED') should return 'Zed' but returned {result!r}."


def test_initials():
    result = _fn("initials")("ada lovelace")
    assert result == "A.L.", f"initials('ada lovelace') should return 'A.L.' but returned {result!r}."


def test_initials_three_names():
    result = _fn("initials")("Jean claude Van")
    assert result == "J.C.V.", f"initials('Jean claude Van') should return 'J.C.V.' but returned {result!r}."


def test_palindromes():
    is_palindrome = _fn("is_palindrome")
    for text in ["racecar", "Racecar", "A man, a plan, a canal: Panama", "No lemon, no melon"]:
        assert is_palindrome(text) is True, f"is_palindrome({text!r}) should be True but was {is_palindrome(text)!r}."


def test_not_palindromes():
    is_palindrome = _fn("is_palindrome")
    for text in ["python", "Hello, world"]:
        assert is_palindrome(text) is False, f"is_palindrome({text!r}) should be False but was {is_palindrome(text)!r}."
