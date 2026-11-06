---
title: "Composition: Objects That Use Objects"
minutes: 18
prereqs: ["08-oop/04-inheritance"]
concepts: ["composition", "has-a", "delegation", "dependency injection", "duck typing", "testability"]
local_only: false
hints:
  - "Engine: __init__(self, horsepower) sets self.horsepower and self.running = False. start sets running to True, stop sets it to False."
  - "Car.__init__(self, name, engine) stores name and engine and sets self.odometer = 0. drive: raise ValueError(\"distance must be positive\") when km <= 0; if not self.engine.running call self.engine.start(); then add km to the odometer. park calls self.engine.stop()."
  - "describe: f\"{self.name}: {self.engine.horsepower} hp, {self.odometer} km\". The Car only uses the engine's start(), stop(), running and horsepower, so any object offering those works, including a fake one in a test."
---

## Why this matters

Inheritance says "is a". But a car is not a kind of engine: it **has** an engine. When one object is built from other objects, that is **composition**, and it is usually the more flexible choice. Prefer composition unless the "is a" relationship is really true.

## The idea

```python
class Battery:
    def __init__(self, charge=100):
        self.charge = charge

    def use(self, amount):
        self.charge -= amount

class Phone:
    def __init__(self, battery):          # the Phone is GIVEN a battery
        self.battery = battery

    def call(self, minutes):
        self.battery.use(minutes * 2)     # delegate the work to the part

phone = Phone(Battery())
phone.call(10)
print(phone.battery.charge)               # 80
```

Passing the parts in (instead of creating them inside) makes the class easy to change and to test: any object that offers `use()` will do. Python cares about what an object *can do*, not what class it is. This is **duck typing**: "if it quacks like a duck...".

## Try it

Make a `SolarBattery` class whose `use` does nothing, and pass it to `Phone`. The phone code does not change.

## Your turn

Write two classes:

- `Engine(horsepower)` with `running` (starts `False`), `start()` and `stop()`.
- `Car(name, engine)` with an `odometer` (starts at `0`) and:
  - `drive(km)`: raise `ValueError("distance must be positive")` for `km <= 0`. If the engine is not running, start it first (once). Add `km` to the odometer.
  - `park()`: stop the engine.
  - `describe()`: text like `Mini: 90 hp, 15 km`.

The checks give your `Car` a *fake* engine to prove it only relies on `start()`, `stop()`, `running` and `horsepower`.

## Recap

- Composition: build objects from other objects ("has a") and delegate to them.
- Pass collaborators in, so they can be swapped or faked.
- Duck typing: what matters is the methods an object has, not its class.

## Common mistakes

- **Creating the part inside the class** (`self.engine = Engine(90)`), which makes it hard to change or test.
- **Reaching deep into the part** (`car.engine.running = True` from outside) instead of calling methods.
- **Using inheritance for a "has-a"**, such as `class Car(Engine)`.
