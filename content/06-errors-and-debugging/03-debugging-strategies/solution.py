def average(numbers):
    return sum(numbers) / len(numbers)


def count_vowels(text):
    count = 0
    for ch in text.lower():
        if ch in "aeiou":
            count += 1
    return count


def last_n(items, n):
    if n <= 0:
        return []
    return items[-n:]


def remove_negatives(numbers):
    return [n for n in numbers if n >= 0]
