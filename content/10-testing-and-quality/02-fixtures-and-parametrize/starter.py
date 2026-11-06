import pytest


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def __len__(self):
        return len(self._items)


# Write below:
#   1. a fixture called `stack` holding 1, 2, 3
#   2. two or more tests that use the fixture
#   3. a parametrized test with three or more value sets
