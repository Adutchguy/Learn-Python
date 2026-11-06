class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


def first_n(iterable, n):
    iterator = iter(iterable)
    items = []
    while len(items) < n:
        try:
            items.append(next(iterator))
        except StopIteration:
            break
    return items
