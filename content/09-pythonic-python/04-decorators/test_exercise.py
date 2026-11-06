def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import pytest


def test_count_calls_counts_and_passes_values_through():
    count_calls = _fn("count_calls")

    @count_calls
    def add(a, b=0):
        """Add two numbers."""
        return a + b

    assert add.calls == 0, "calls should start at 0"
    assert add(2, 3) == 5, "the wrapper must return the real function's result"
    assert add(4, b=1) == 5, "keyword arguments must pass through"
    assert add.calls == 2, f"after two calls, calls should be 2, got {add.calls}"


def test_count_calls_keeps_the_function_identity():
    count_calls = _fn("count_calls")

    @count_calls
    def documented():
        """I have a docstring."""

    assert documented.__name__ == "documented", f"use functools.wraps so the name stays 'documented', got {documented.__name__!r}"
    assert documented.__doc__ == "I have a docstring.", "use functools.wraps so the docstring is kept"


def test_separate_functions_have_separate_counters():
    count_calls = _fn("count_calls")

    @count_calls
    def one():
        return 1

    @count_calls
    def two():
        return 2

    one()
    one()
    two()
    assert (one.calls, two.calls) == (2, 1), f"each decorated function needs its own counter, got {(one.calls, two.calls)!r}"


def _flaky(failures, error=ValueError):
    state = {"attempts": 0}

    def func(value):
        """Fails a few times, then works."""
        state["attempts"] += 1
        if state["attempts"] <= failures:
            raise error(f"failure {state['attempts']}")
        return value * 2

    return func, state


def test_retry_succeeds_after_some_failures():
    retry = _fn("retry")
    func, state = _flaky(2)
    wrapped = retry(3)(func)
    assert wrapped(21) == 42, "after two failures the third attempt works, so the result 42 should be returned"
    assert state["attempts"] == 3, f"it should have made exactly 3 attempts, made {state['attempts']}"


def test_retry_stops_after_success():
    retry = _fn("retry")
    func, state = _flaky(0)
    wrapped = retry(5)(func)
    assert wrapped(1) == 2, "a first-try success returns the result"
    assert state["attempts"] == 1, f"do not retry after a success, but it made {state['attempts']} attempts"


def test_retry_gives_up_and_reraises_the_last_error():
    retry = _fn("retry")
    func, state = _flaky(10, error=KeyError)
    wrapped = retry(3)(func)
    with pytest.raises(KeyError):
        wrapped(1)
    assert state["attempts"] == 3, f"it should try exactly 3 times before giving up, tried {state['attempts']}"


def test_retry_with_one_attempt_and_decorator_syntax():
    retry = _fn("retry")

    @retry(1)
    def always_fails():
        """Documented."""
        raise RuntimeError("no")

    assert always_fails.__name__ == "always_fails", "retry should use functools.wraps to keep the name"
    with pytest.raises(RuntimeError):
        always_fails()
