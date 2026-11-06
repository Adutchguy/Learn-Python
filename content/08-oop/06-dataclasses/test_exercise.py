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


import dataclasses


def test_product_is_a_dataclass_with_a_readable_repr():
    Product = _cls("Product")
    assert dataclasses.is_dataclass(Product), "Product should be a dataclass: put @dataclass above the class."
    assert repr(Product("Tea", 2.5)) == "Product(name='Tea', price=2.5, tags=[])", f"repr(Product('Tea', 2.5)) should be \"Product(name='Tea', price=2.5, tags=[])\" but was {repr(Product('Tea', 2.5))!r}."


def test_product_equality_and_tags():
    Product = _cls("Product")
    assert Product("Tea", 2.5) == Product("Tea", 2.5), "Two products with the same fields should be equal."
    assert Product("Tea", 2.5, ["hot"]).tags == ["hot"], "tags can be given."
    a, b = Product("A", 1.0), Product("B", 1.0)
    a.tags.append("x")
    assert b.tags == [], f"Each product needs its own tags list, but the second one has {b.tags!r}. Use field(default_factory=list)."


def test_product_validates_the_price():
    import pytest

    Product = _cls("Product")
    with pytest.raises(ValueError) as info:
        Product("Bad", -1.0)
    assert str(info.value) == "price cannot be negative", f"The message should be 'price cannot be negative' but was {str(info.value)!r}."
    assert Product("Free", 0).price == 0, "A price of 0 is allowed."


def test_price_with_tax():
    Product = _cls("Product")
    assert Product("Tea", 2.5).price_with_tax(0.2) == 3.0, f"2.5 plus 20% tax is 3.0 but you returned {Product('Tea', 2.5).price_with_tax(0.2)!r}."
    assert Product("Pen", 1.99).price_with_tax(0.1) == 2.19, f"1.99 plus 10% tax is 2.19 (rounded) but you returned {Product('Pen', 1.99).price_with_tax(0.1)!r}."


def test_coordinate_is_frozen_and_hashable():
    import pytest

    Coordinate = _cls("Coordinate")
    c = Coordinate(1.5, 2.5)
    assert (c.lat, c.lon) == (1.5, 2.5), "Coordinate(1.5, 2.5) should store lat and lon."
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.lat = 9
    places = {Coordinate(1, 2): "home"}
    assert places[Coordinate(1, 2)] == "home", "Equal frozen coordinates should work as the same dictionary key."


def test_tasks_sort_by_priority():
    Task = _cls("Task")
    tasks = [Task(3, "sleep"), Task(1, "eat"), Task(2, "code")]
    assert [t.priority for t in sorted(tasks)] == [1, 2, 3], f"sorted(tasks) should order by priority but gave {[t.priority for t in sorted(tasks)]!r}. Use @dataclass(order=True)."
    assert Task(1, "zebra") < Task(2, "apple"), "Only the priority is compared, not the title."
    assert min(tasks).title == "eat", f"min(tasks) should be the 'eat' task but was {min(tasks)!r}."
