from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    tags: list = field(default_factory=list)

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("price cannot be negative")

    def price_with_tax(self, rate):
        return round(self.price * (1 + rate), 2)


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float


@dataclass(order=True)
class Task:
    priority: int
    title: str = field(compare=False)
