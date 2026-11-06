from collections import Counter, defaultdict, deque


def top_words(text, n):
    counts = Counter(text.lower().split())
    return counts.most_common(n)


def group_by_length(words):
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)


def rotate(items, k):
    d = deque(items)
    d.rotate(k)
    return list(d)
