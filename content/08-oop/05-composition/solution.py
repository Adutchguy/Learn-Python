class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


class Car:
    def __init__(self, name, engine):
        self.name = name
        self.engine = engine
        self.odometer = 0

    def drive(self, km):
        if km <= 0:
            raise ValueError("distance must be positive")
        if not self.engine.running:
            self.engine.start()
        self.odometer += km

    def park(self):
        self.engine.stop()

    def describe(self):
        return f"{self.name}: {self.engine.horsepower} hp, {self.odometer} km"
