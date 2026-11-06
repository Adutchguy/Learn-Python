def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _cls(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a class called {name}. Start it with: class {name}:"
    cls = getattr(exercise, name)
    assert isinstance(cls, type), f"{name} should be a class, but it is {cls!r}."
    return cls


def test_point_defaults_and_values():
    Point = _cls("Point")
    origin = Point()
    assert (origin.x, origin.y) == (0, 0), f"Point() should have x == 0 and y == 0 but has x == {origin.x!r} and y == {origin.y!r}."
    p = Point(3, 4)
    assert (p.x, p.y) == (3, 4), f"Point(3, 4) should have x == 3 and y == 4 but has x == {p.x!r} and y == {p.y!r}."
    assert Point(y=7).x == 0 and Point(y=7).y == 7, "Point(y=7) should keep the default x == 0."


def test_points_are_independent():
    Point = _cls("Point")
    a, b = Point(1, 1), Point(1, 1)
    a.x = 99
    assert b.x == 1, "Changing one Point must not change another. Store the values on self."


def test_book_attributes():
    Book = _cls("Book")
    book = Book("Dune", "Herbert", 412)
    assert (book.title, book.author, book.pages) == ("Dune", "Herbert", 412), f"The Book's attributes are wrong: {(book.title, book.author, book.pages)!r}."
    assert book.pages_read == 0, f"pages_read should start at 0 but is {book.pages_read!r}."
    assert book.notes == [], f"notes should start as an empty list but is {book.notes!r}."


def test_each_book_has_its_own_notes():
    Book = _cls("Book")
    first, second = Book("A", "x", 1), Book("B", "y", 2)
    first.notes.append("great")
    assert second.notes == [], f"The second book's notes should still be empty but are {second.notes!r}. Create the list inside __init__ with self.notes = []."


def test_make_library():
    Book = _cls("Book")
    make_library = _fn("make_library")
    library = make_library([("Dune", "Herbert", 412), ("Emma", "Austen", 320)])
    assert len(library) == 2, f"make_library should return 2 books but returned {len(library)}."
    assert all(isinstance(b, Book) for b in library), "make_library should return Book objects."
    assert [b.title for b in library] == ["Dune", "Emma"], f"The books should be in the same order as the rows, but the titles are {[b.title for b in library]!r}."
    assert make_library([]) == [], "No rows gives an empty list."
