def apply_twice(func, value):
    return func(func(value))


def sort_people(people):
    return sorted(people, key=lambda person: person[1], reverse=True)


def longest(words):
    return max(words, key=len)
