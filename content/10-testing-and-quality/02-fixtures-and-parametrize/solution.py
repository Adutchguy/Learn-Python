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


@pytest.fixture
def stack():
    s = Stack()
    for number in (1, 2, 3):
        s.push(number)
    return s


def test_peek_shows_the_top(stack):
    assert stack.peek() == 3


def test_pop_removes_the_top(stack):
    assert stack.pop() == 3
    assert len(stack) == 2


@pytest.mark.parametrize("value", [1, "text", None, 2.5])
def test_push_then_pop_returns_the_same_value(value):
    s = Stack()
    s.push(value)
    assert s.pop() == value
