# Charts with Matplotlib

*Optional track: Data Analysis · about 22 minutes*

> This lesson uses matplotlib. Install them once with `pip install -r requirements-tracks.txt`.

## Why this matters

A good chart shows a pattern in seconds that a table of numbers hides. **Matplotlib** is Python's most widely used plotting library, and many other tools (pandas plotting, seaborn) are built on it. This lesson runs on your own computer, because charts open in a window or are saved as picture files.

Install the extras once with `pip install -r requirements-tracks.txt`.

## The idea

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()           # a Figure (the canvas) and an Axes (one chart on it)
ax.plot([1, 2, 3, 4], [10, 12, 9, 15])      # x values, then y values: a line chart
ax.set_title("Daily steps")
ax.set_xlabel("Day")
ax.set_ylabel("Steps (hundreds)")
plt.show()                          # opens a window (on your own computer)
```

- `fig` is the whole picture; `ax` is the chart inside it. You draw on the **Axes** and label it with `set_title`, `set_xlabel` and `set_ylabel`.
- A **bar chart** is `ax.bar(labels, heights)`. A **scatter plot** is `ax.scatter(xs, ys)`. A **histogram** is `ax.hist(values)`.
- `fig.savefig("steps.png")` writes the chart to an image file instead of (or as well as) showing it. Do this in scripts that run without a screen.

Always label what the chart shows: a title, axis labels with units, and a legend (`ax.legend()`, with `label=` on each plot) when there are several lines.

pandas can draw straight from a table too (`df.plot(...)`), and it returns the same Axes object.

## Try it

Plot the numbers 1 to 5 against their squares and show the chart with `plt.show()`. Then change it to a bar chart.

## Your turn

The checks run without opening a window and inspect the chart you built. Write:

- `line_chart(days, values)`: a line chart of `values` against `days`, titled `"Daily steps"`, with the x label `"Day"` and the y label `"Steps"`. Return the Axes.
- `bar_chart(labels, counts)`: a bar chart with one bar per label, titled `"Votes"`. Return the Axes.
- `save_chart(ax, path)`: save the chart to the file `path` as an image.

## Recap

- `fig, ax = plt.subplots()` makes the canvas and one chart; you draw and label on `ax`.
- `plot` (lines), `bar`, `scatter` and `hist` are the everyday chart types.
- `plt.show()` shows a window; `fig.savefig(path)` writes a file.
- Titles, axis labels and units are part of the chart, not extras.

## Common mistakes

- **Forgetting `plt.show()` or `savefig`** in a script, so nothing appears.
- **Mixing the older `plt.plot(...)` style with `ax.plot(...)`** and drawing on the wrong chart. Pick one; the Axes style scales better.
- **Unlabelled axes.** A chart without units is a puzzle, not a message.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/11-data-analysis/07-charts-with-matplotlib
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

line_chart: fig, ax = plt.subplots() gives a blank chart. ax.plot(days, values) draws the line, then ax.set_title("Daily steps"), ax.set_xlabel("Day"), ax.set_ylabel("Steps"). Return ax.

</details>

<details><summary>Hint 2</summary>

bar_chart: ax.bar(labels, counts) draws one bar per label. Give the chart the title "Votes" with ax.set_title and return ax.

</details>

<details><summary>Hint 3</summary>

save_chart: the figure that owns an Axes is ax.figure. ax.figure.savefig(path) writes the picture to a file (a .png path makes a PNG image).

</details>
