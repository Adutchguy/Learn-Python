import functools
import operator


def power(base, exp):
    return base ** exp


# Add:
#   fib(n)            -> fast recursive Fibonacci (use functools.cache)
#   square, cube      -> functools.partial of power
#   product(numbers)  -> functools.reduce with operator.mul
