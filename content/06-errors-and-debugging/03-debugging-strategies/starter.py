# Each function has a bug. Find it and fix it.

def average(numbers):
    return sum(numbers) / (len(numbers) + 1)


def count_vowels(text):
    count = 0
    for ch in text:
        if ch in "aeiou":
            count += 1
    return count


def last_n(items, n):
    return items[-n:]


def remove_negatives(numbers):
    for n in numbers:
        if n < 0:
            numbers.remove(n)
    return numbers
