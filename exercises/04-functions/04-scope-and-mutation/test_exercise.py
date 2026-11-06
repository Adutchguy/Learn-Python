def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_add_tax():
    result = _fn("add_tax")(10)
    assert result == 12.0, f"add_tax(10) with a 20% rate should return 12.0 but returned {result!r}."


def test_add_tax_rounds_to_two_places():
    result = _fn("add_tax")(9.99)
    assert result == 11.99, f"add_tax(9.99) should return 11.99 (rounded to 2 places) but returned {result!r}."


def test_add_tax_reads_the_current_rate(monkeypatch):
    func = _fn("add_tax")
    monkeypatch.setattr("exercise.TAX_RATE", 0.5)
    result = func(10)
    assert result == 15.0, (
        f"With TAX_RATE set to 0.5, add_tax(10) should return 15.0 but returned {result!r}. "
        "Use the TAX_RATE variable inside the function instead of typing 0.2."
    )


def test_with_item_returns_the_new_list():
    result = _fn("with_item")(["milk"], "eggs")
    assert result == ["milk", "eggs"], f"with_item(['milk'], 'eggs') should return ['milk', 'eggs'] but returned {result!r}."


def test_with_item_leaves_the_original_alone():
    cart = ["milk"]
    _fn("with_item")(cart, "eggs")
    assert cart == ["milk"], f"with_item must not change the list it is given, but cart is now {cart!r}."


def test_with_item_returns_a_different_list():
    cart = ["milk"]
    result = _fn("with_item")(cart, "eggs")
    assert result is not cart, "with_item should return a new list, not the same list object that was passed in."
