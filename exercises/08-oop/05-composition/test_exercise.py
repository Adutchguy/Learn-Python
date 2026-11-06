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


class FakeEngine:
    """Records how the Car uses it. Not a real Engine, but it quacks like one."""

    def __init__(self):
        self.horsepower = 100
        self.running = False
        self.calls = []

    def start(self):
        self.running = True
        self.calls.append("start")

    def stop(self):
        self.running = False
        self.calls.append("stop")


def test_engine():
    Engine = _cls("Engine")
    engine = Engine(90)
    assert engine.horsepower == 90, f"Engine(90).horsepower should be 90 but was {engine.horsepower!r}."
    assert engine.running is False, "A new engine is not running."
    engine.start()
    assert engine.running is True, "start() should make running True."
    engine.stop()
    assert engine.running is False, "stop() should make running False."


def test_driving_starts_the_engine_once():
    Car = _cls("Car")
    fake = FakeEngine()
    car = Car("Tiny", fake)
    car.drive(10)
    car.drive(5)
    assert fake.calls == ["start"], f"The engine should be started once, on the first drive, but the calls were {fake.calls!r}."
    assert car.odometer == 15, f"After driving 10 and 5 km the odometer should be 15 but is {car.odometer!r}."


def test_parking_stops_the_engine():
    Car = _cls("Car")
    fake = FakeEngine()
    car = Car("Tiny", fake)
    car.drive(1)
    car.park()
    assert fake.calls == ["start", "stop"], f"The calls should be ['start', 'stop'] but were {fake.calls!r}."
    car.drive(1)
    assert fake.calls == ["start", "stop", "start"], f"Driving again after parking should start the engine again, but the calls were {fake.calls!r}."


def test_describe_uses_the_engine():
    Car = _cls("Car")
    car = Car("Tiny", FakeEngine())
    car.drive(15)
    assert car.describe() == "Tiny: 100 hp, 15 km", f"describe() should be 'Tiny: 100 hp, 15 km' but was {car.describe()!r}."


def test_drive_rejects_bad_distances():
    import pytest

    Car = _cls("Car")
    fake = FakeEngine()
    car = Car("Tiny", fake)
    for km in [0, -5]:
        with pytest.raises(ValueError) as info:
            car.drive(km)
        assert str(info.value) == "distance must be positive", f"drive({km}) should raise ValueError('distance must be positive') but the message was {str(info.value)!r}."
    assert fake.calls == [] and car.odometer == 0, "A rejected drive must not start the engine or change the odometer."


def test_works_with_a_real_engine():
    Engine, Car = _cls("Engine"), _cls("Car")
    engine = Engine(90)
    car = Car("Mini", engine)
    car.drive(15)
    assert engine.running is True, "After driving, the real engine should be running."
    assert car.describe() == "Mini: 90 hp, 15 km", f"describe() should be 'Mini: 90 hp, 15 km' but was {car.describe()!r}."
    car.park()
    assert engine.running is False, "After parking, the real engine should be stopped."
