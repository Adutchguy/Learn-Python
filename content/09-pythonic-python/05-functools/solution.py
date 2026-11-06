import functools
import operator


def power(base, exp):
    return base ** exp


@functools.cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


square = functools.partial(power, exp=2)
cube = functools.partial(power, exp=3)


def product(numbers):
    return functools.reduce(operator.mul, numbers, 1)
