def power(base, exponent=2):
    return base ** exponent


def join_words(*words, sep=" "):
    return sep.join(words)


def profile(name, **details):
    if not details:
        return name
    pairs = [f"{key}={value}" for key, value in sorted(details.items())]
    return f"{name} ({', '.join(pairs)})"
