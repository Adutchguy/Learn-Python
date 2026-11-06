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


import pytest


def test_shape_is_abstract():
    Shape = _cls("Shape")
    with pytest.raises(TypeError):
        Shape()


def test_an_incomplete_subclass_cannot_be_created():
    Shape = _cls("Shape")

    class Half(Shape):
        def area(self):
            return 1

    with pytest.raises(TypeError):
        Half()


def test_square():
    Shape, Square = _cls("Shape"), _cls("Square")
    s = Square(3)
    assert isinstance(s, Shape), "Square should inherit from Shape."
    assert s.area() == 9, f"Square(3).area() should be 9 but was {s.area()!r}."
    assert s.perimeter() == 12, f"Square(3).perimeter() should be 12 but was {s.perimeter()!r}."


def test_circle():
    Shape, Circle = _cls("Shape"), _cls("Circle")
    c = Circle(1)
    assert isinstance(c, Shape), "Circle should inherit from Shape."
    assert c.area() == pytest.approx(3.14159265), f"Circle(1).area() should be about 3.14159 but was {c.area()!r}."
    assert Circle(2).perimeter() == pytest.approx(12.5663706), f"Circle(2).perimeter() should be about 12.5664 but was {Circle(2).perimeter()!r}."


def test_largest():
    Square, Circle = _cls("Square"), _cls("Circle")
    largest = _fn("largest")
    small, big = Square(2), Circle(2)
    assert largest([small, big]) is big, "The circle of radius 2 (area about 12.6) is larger than a square of side 2 (area 4)."
    assert largest([Square(5), Circle(1)]).area() == 25, "The square of side 5 (area 25) is the largest here."


def test_total_area_accepts_any_object_with_an_area_method():
    Square = _cls("Square")
    total_area = _fn("total_area")

    class Blob:  # not a Shape at all, but it quacks like one
        def area(self):
            return 5

    assert total_area([Square(2), Blob()]) == 9, f"total_area([Square(2), Blob()]) should be 4 + 5 = 9 but was {total_area([Square(2), Blob()])!r}. Do not check types: just call area()."
    assert total_area([]) == 0, "No things have a total area of 0."
