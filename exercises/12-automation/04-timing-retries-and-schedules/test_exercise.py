def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _cls(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a class called {name}. Start it with: class {name}:"
    cls = getattr(exercise, name)
    assert isinstance(cls, type), f"{name} should be a class, but it is {cls!r}."
    return cls


from datetime import datetime


class _FakeClock:
    def __init__(self, *times):
        self.times = list(times)

    def __call__(self):
        return self.times.pop(0)


class _Flaky:
    """Fails the first `failures` times it is called, then returns 'ok'."""

    def __init__(self, failures):
        self.failures = failures
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self.calls <= self.failures:
            raise ConnectionError(f"attempt {self.calls} failed")
        return "ok"


def test_stopwatch_measures_with_the_given_clock():
    watch = _cls("Stopwatch")(clock=_FakeClock(10.0, 12.5))
    watch.start()
    elapsed = watch.stop()
    assert elapsed == 2.5, f"The clock said 10.0 at start and 12.5 at stop, so stop() should return 2.5 but returned {elapsed!r}. Call self.clock() rather than time.perf_counter()."


def test_stopwatch_works_with_the_real_clock():
    watch = _cls("Stopwatch")()
    watch.start()
    elapsed = watch.stop()
    assert isinstance(elapsed, float) and 0 <= elapsed < 1, f"With the real clock stop() should give a small number of seconds but gave {elapsed!r}."


def test_retry_returns_the_first_success_without_sleeping():
    naps = []
    func = _Flaky(0)
    result = _fn("retry")(func, 3, 1, sleep=naps.append)
    assert result == "ok" and func.calls == 1, f"A function that works first time should be called once and its result returned. Result {result!r}, calls {func.calls}."
    assert naps == [], f"There is nothing to wait for when the first try works but retry slept for {naps}."


def test_retry_waits_longer_each_time():
    naps = []
    func = _Flaky(2)
    result = _fn("retry")(func, 5, 1, sleep=naps.append)
    assert result == "ok", f"The third call works, so retry should return 'ok' but returned {result!r}."
    assert func.calls == 3, f"The function should be called 3 times but was called {func.calls}."
    assert naps == [1, 2], f"The waits should be [1, 2] (the delay doubles) but were {naps}."


def test_retry_gives_up_and_raises_the_last_error():
    import pytest

    naps = []
    func = _Flaky(10)
    with pytest.raises(ConnectionError) as info:
        _fn("retry")(func, 3, 1, sleep=naps.append)
    assert func.calls == 3, f"With attempts=3 the function should be tried 3 times but was tried {func.calls}."
    assert "attempt 3" in str(info.value), f"The error from the LAST attempt should be raised but it was: {info.value}"
    assert naps == [1, 2], f"There should be a wait after each failure except the last: [1, 2] but the waits were {naps}."


def test_next_runs_spaces_the_times():
    start = datetime(2026, 1, 1, 9, 0)
    result = _fn("next_runs")(start, 45, 4)
    want = [datetime(2026, 1, 1, 9, 0), datetime(2026, 1, 1, 9, 45), datetime(2026, 1, 1, 10, 30), datetime(2026, 1, 1, 11, 15)]
    assert result == want, f"Expected {[str(t) for t in want]} but got {[str(t) for t in result]}."


def test_next_runs_crosses_midnight():
    result = _fn("next_runs")(datetime(2026, 12, 31, 23, 30), 60, 3)
    assert result[-1] == datetime(2027, 1, 1, 1, 30), f"The third run should be 2027-01-01 01:30 but is {result[-1]}."


def test_run_every_waits_between_calls_only():
    naps = []
    counter = iter(range(100))
    results = _fn("run_every")(lambda: next(counter), 30, 4, sleep=naps.append)
    assert results == [0, 1, 2, 3], f"It should return the result of every call [0, 1, 2, 3] but returned {results}."
    assert naps == [30, 30, 30], f"With 4 calls there are 3 gaps, so 3 sleeps of 30, but the sleeps were {naps}."
