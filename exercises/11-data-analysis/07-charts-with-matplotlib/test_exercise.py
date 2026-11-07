def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import os

# Draw without opening a window, so the checks also work on a computer with no screen.
os.environ["MPLBACKEND"] = "Agg"


def _close_all():
    import matplotlib.pyplot as plt

    plt.close("all")


def test_line_chart_draws_the_data():
    ax = _fn("line_chart")([1, 2, 3], [4000, 5200, 3900])
    assert len(ax.lines) == 1, f"The chart should have exactly one line but has {len(ax.lines)}. Use ax.plot(days, values) once."
    line = ax.lines[0]
    assert list(line.get_xdata()) == [1, 2, 3], f"The x values should be [1, 2, 3] but are {list(line.get_xdata())}."
    assert list(line.get_ydata()) == [4000, 5200, 3900], f"The y values should be [4000, 5200, 3900] but are {list(line.get_ydata())}."
    _close_all()


def test_line_chart_is_labelled():
    ax = _fn("line_chart")([1, 2], [3, 4])
    assert ax.get_title() == "Daily steps", f"The title should be 'Daily steps' but is {ax.get_title()!r}. Use ax.set_title(...)."
    assert ax.get_xlabel() == "Day", f"The x label should be 'Day' but is {ax.get_xlabel()!r}. Use ax.set_xlabel(...)."
    assert ax.get_ylabel() == "Steps", f"The y label should be 'Steps' but is {ax.get_ylabel()!r}. Use ax.set_ylabel(...)."
    _close_all()


def test_bar_chart_has_one_bar_per_label():
    ax = _fn("bar_chart")(["red", "green", "blue"], [3, 5, 2])
    heights = [patch.get_height() for patch in ax.patches]
    assert heights == [3, 5, 2], f"The bar heights should be [3, 5, 2] but are {heights}. Use ax.bar(labels, counts)."
    ax.figure.canvas.draw()
    labels = [t.get_text() for t in ax.get_xticklabels()]
    assert labels == ["red", "green", "blue"], f"The bars should be labelled ['red', 'green', 'blue'] but are labelled {labels}."
    _close_all()


def test_bar_chart_title():
    ax = _fn("bar_chart")(["a"], [1])
    assert ax.get_title() == "Votes", f"The title should be 'Votes' but is {ax.get_title()!r}."
    _close_all()


def test_save_chart_writes_a_png(tmp_path):
    ax = _fn("bar_chart")(["a", "b"], [1, 2])
    path = tmp_path / "votes.png"
    _fn("save_chart")(ax, str(path))
    assert path.exists(), "save_chart should create the file. Use ax.figure.savefig(path)."
    assert path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", "The file should be a PNG image. Save to a path that ends in .png."
    _close_all()
