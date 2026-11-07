def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _close(result, expected, what):
    import numpy as np

    assert isinstance(result, np.ndarray), (
        f"{what} should return a NumPy array (np.ndarray) but returned {type(result).__name__}. "
        "Wrap your list with np.array(...) and use array arithmetic."
    )
    got = result.tolist()
    assert len(got) == len(expected) and all(abs(a - b) < 1e-9 for a, b in zip(got, expected)), (
        f"{what} should return {expected} but returned {got}."
    )


def test_celsius_to_fahrenheit():
    _close(_fn("celsius_to_fahrenheit")([0, 100, -40, 37]), [32, 212, -40, 98.6], "celsius_to_fahrenheit([0, 100, -40, 37])")


def test_normalise_spans_zero_to_one():
    _close(_fn("normalise")([10, 20, 30]), [0, 0.5, 1], "normalise([10, 20, 30])")
    _close(_fn("normalise")([5, 1, 3]), [1, 0, 0.5], "normalise([5, 1, 3])")


def test_above_average_keeps_only_larger_values():
    _close(_fn("above_average")([1, 2, 3, 10]), [10], "above_average([1, 2, 3, 10])")
    _close(_fn("above_average")([5, 9, 1, 7]), [9, 7], "above_average([5, 9, 1, 7])")


def test_above_average_with_equal_values_keeps_nothing():
    _close(_fn("above_average")([4, 4, 4]), [], "above_average([4, 4, 4]) (nothing is above the average)")


def test_column_means():
    _close(_fn("column_means")([[1, 2, 3], [4, 5, 6]]), [2.5, 3.5, 4.5], "column_means([[1, 2, 3], [4, 5, 6]])")
    _close(_fn("column_means")([[10, 0], [20, 0], [30, 6]]), [20, 2], "column_means of three rows")


def test_no_python_loops():
    import ast
    import inspect

    import exercise

    for name in ("celsius_to_fahrenheit", "normalise", "above_average", "column_means"):
        source = inspect.getsource(getattr(exercise, name))
        tree = ast.parse(source)
        loops = [n for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While, ast.ListComp))]
        assert not loops, (
            f"{name} uses a loop or list comprehension. The point of NumPy is that one expression "
            "works on the whole array at once, so try array arithmetic instead."
        )
