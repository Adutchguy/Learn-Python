class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.pages_read = 0
        self.notes = []


def make_library(rows):
    return [Book(title, author, pages) for title, author, pages in rows]
