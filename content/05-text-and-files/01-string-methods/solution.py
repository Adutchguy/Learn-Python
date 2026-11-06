def clean_name(raw):
    return " ".join(word.capitalize() for word in raw.split())


def initials(name):
    result = ""
    for word in name.split():
        result += word[0].upper() + "."
    return result


def is_palindrome(text):
    letters = ""
    for ch in text.lower():
        if ch.isalpha():
            letters += ch
    return letters == letters[::-1]
