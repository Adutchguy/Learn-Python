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


def _filled():
    Cart = _cls("Cart")
    cart = Cart()
    cart.add("apple", 0.5, 4)
    cart.add("bread", 2.25)
    return cart


def test_total_and_count():
    cart = _filled()
    assert cart.total() == 4.25, f"total() should be 4.25 (4 apples at 0.50 plus 1 bread at 2.25) but was {cart.total()!r}."
    assert cart.count() == 5, f"count() should be 5 but was {cart.count()!r}."


def test_adding_the_same_item_again_increases_quantity():
    cart = _filled()
    cart.add("apple", 0.5, 2)
    assert cart.count() == 7, f"After adding 2 more apples count() should be 7 but was {cart.count()!r}."
    assert cart.total() == 5.25, f"After adding 2 more apples total() should be 5.25 but was {cart.total()!r}."


def test_remove():
    import pytest

    cart = _filled()
    cart.remove("bread")
    assert cart.total() == 2.0, f"After removing the bread total() should be 2.0 but was {cart.total()!r}."
    assert cart.count() == 4, f"After removing the bread count() should be 4 but was {cart.count()!r}."
    with pytest.raises(KeyError):
        cart.remove("ghost")


def test_most_expensive():
    cart = _filled()
    assert cart.most_expensive() == "bread", f"most_expensive() should be 'bread' but was {cart.most_expensive()!r}."
    cart.add("cheese", 9.0)
    assert cart.most_expensive() == "cheese", f"most_expensive() should be 'cheese' after adding it, but was {cart.most_expensive()!r}."


def test_empty_cart():
    Cart = _cls("Cart")
    cart = Cart()
    assert cart.total() == 0, f"An empty cart's total() should be 0 but was {cart.total()!r}."
    assert cart.count() == 0, f"An empty cart's count() should be 0 but was {cart.count()!r}."
    assert cart.most_expensive() is None, f"An empty cart's most_expensive() should be None but was {cart.most_expensive()!r}."


def test_carts_are_independent():
    Cart = _cls("Cart")
    a, b = Cart(), Cart()
    a.add("x", 1.0)
    assert b.count() == 0, "A second cart must start empty. Create the dictionary inside __init__ (self.items = {})."
