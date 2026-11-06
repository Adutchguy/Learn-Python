def average(numbers):
    return sum(numbers) / len(numbers)


def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


def min_max(numbers):
    return min(numbers), max(numbers)
