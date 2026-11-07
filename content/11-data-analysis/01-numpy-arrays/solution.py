import numpy as np


def celsius_to_fahrenheit(temps):
    return np.array(temps) * 9 / 5 + 32


def normalise(values):
    values = np.array(values, dtype=float)
    return (values - values.min()) / (values.max() - values.min())


def above_average(values):
    values = np.array(values)
    return values[values > values.mean()]


def column_means(rows):
    return np.array(rows).mean(axis=0)
