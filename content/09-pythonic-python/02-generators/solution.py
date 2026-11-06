def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def chunks(items, size):
    if size < 1:
        raise ValueError("size must be at least 1")
    for start in range(0, len(items), size):
        yield items[start:start + size]


def running_total(numbers):
    total = 0
    for number in numbers:
        total += number
        yield total
