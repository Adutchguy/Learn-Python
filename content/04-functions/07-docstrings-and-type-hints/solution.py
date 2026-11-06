def bmi(weight: float, height: float) -> float:
    """Return the body mass index for a weight in kg and a height in metres."""
    return weight / (height ** 2)


def to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32
