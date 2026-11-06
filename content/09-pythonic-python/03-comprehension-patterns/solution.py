def flatten(matrix):
    return [item for row in matrix for item in row]


def invert(d):
    return {value: key for key, value in d.items()}


def unique_lengths(words):
    return {len(word) for word in words}


def label_parity(numbers):
    return ["even" if n % 2 == 0 else "odd" for n in numbers]


def all_positive(numbers):
    return all(n > 0 for n in numbers)


def any_long(words, size):
    return any(len(word) >= size for word in words)
