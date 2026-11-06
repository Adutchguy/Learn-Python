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


def test_temperature_conversions():
    Temperature = _cls("Temperature")
    t = Temperature(25)
    assert t.celsius == 25, f"t.celsius should be 25 but was {t.celsius!r}."
    assert t.fahrenheit == 77.0, f"25 C is 77 F but t.fahrenheit was {t.fahrenheit!r}. Reading fahrenheit should not need parentheses."
    assert t.kelvin == pytest.approx(298.15), f"25 C is 298.15 K but t.kelvin was {t.kelvin!r}."


def test_setting_fahrenheit_changes_celsius():
    Temperature = _cls("Temperature")
    t = Temperature(0)
    t.fahrenheit = 212
    assert t.celsius == pytest.approx(100), f"After t.fahrenheit = 212 the celsius value should be 100 but was {t.celsius!r}."
    t.celsius = -40
    assert t.fahrenheit == pytest.approx(-40), "-40 C is -40 F."


def test_absolute_zero_is_enforced_everywhere():
    Temperature = _cls("Temperature")
    with pytest.raises(ValueError) as info:
        Temperature(-300)
    assert "absolute zero" in str(info.value), f"The message should mention 'absolute zero' but was {str(info.value)!r}."
    t = Temperature(10)
    with pytest.raises(ValueError):
        t.celsius = -500
    with pytest.raises(ValueError):
        t.fahrenheit = -1000
    assert t.celsius == 10, f"A rejected value must not change the temperature, but celsius is now {t.celsius!r}."


def test_kelvin_is_read_only():
    Temperature = _cls("Temperature")
    t = Temperature(0)
    with pytest.raises(AttributeError):
        t.kelvin = 5


def test_rectangle_computed_properties():
    Rectangle = _cls("Rectangle")
    r = Rectangle(3, 4)
    assert r.area == 12, f"Rectangle(3, 4).area should be 12 but was {r.area!r}."
    assert r.perimeter == 14, f"Rectangle(3, 4).perimeter should be 14 but was {r.perimeter!r}."
    assert r.is_square is False, "A 3 by 4 rectangle is not a square."
    assert Rectangle(5, 5).is_square is True, "A 5 by 5 rectangle is a square."


def test_rectangle_properties_stay_up_to_date_and_read_only():
    Rectangle = _cls("Rectangle")
    r = Rectangle(3, 4)
    r.width = 10
    assert r.area == 40, f"After setting width to 10 the area should be 40 but was {r.area!r}. Compute it from the current width and height."
    with pytest.raises(AttributeError):
        r.area = 99
