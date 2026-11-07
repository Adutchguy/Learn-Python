import matplotlib.pyplot as plt


def line_chart(days, values):
    fig, ax = plt.subplots()
    ax.plot(days, values)
    ax.set_title("Daily steps")
    ax.set_xlabel("Day")
    ax.set_ylabel("Steps")
    return ax


def bar_chart(labels, counts):
    fig, ax = plt.subplots()
    ax.bar(labels, counts)
    ax.set_title("Votes")
    return ax


def save_chart(ax, path):
    ax.figure.savefig(path)
