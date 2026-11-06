def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import asyncio
import inspect
import time


def test_fetch_is_a_coroutine_function_that_returns_text():
    fetch = _fn("fetch")
    assert inspect.iscoroutinefunction(fetch), "fetch should be defined with async def"
    assert asyncio.run(fetch("a", 0)) == "a done", "fetch('a', 0) should return 'a done'"


def test_fetch_all_is_a_coroutine_function_and_keeps_order():
    fetch_all = _fn("fetch_all")
    assert inspect.iscoroutinefunction(fetch_all), "fetch_all should be defined with async def"
    result = asyncio.run(fetch_all([("slow", 0.2), ("fast", 0.0)]))
    assert result == ["slow done", "fast done"], f"results should be in the order of the jobs, not the order they finish; got {result!r}"


def test_run_all_is_a_normal_function():
    run_all = _fn("run_all")
    assert not inspect.iscoroutinefunction(run_all), "run_all should be an ordinary def that calls asyncio.run"
    assert run_all([("x", 0), ("y", 0)]) == ["x done", "y done"], "run_all should return the list of results"
    assert run_all([]) == [], "no jobs should give an empty list"


def test_jobs_run_at_the_same_time():
    run_all = _fn("run_all")
    started = time.perf_counter()
    results = run_all([("a", 0.3), ("b", 0.3), ("c", 0.3)])
    elapsed = time.perf_counter() - started
    assert results == ["a done", "b done", "c done"], f"unexpected results {results!r}"
    assert elapsed < 0.7, f"three 0.3-second jobs took {elapsed:.2f} s: they ran one after another. Use asyncio.gather to run them together."
