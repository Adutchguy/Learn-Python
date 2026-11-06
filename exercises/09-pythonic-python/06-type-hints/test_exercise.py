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


import collections.abc
import typing


def _hints(name):
    return typing.get_type_hints(_fn(name))


def test_average_hints():
    hints = _hints("average")
    assert hints.get("numbers") == list[float], f"numbers should be list[float], found {hints.get('numbers')!r}"
    assert hints.get("return") is float, f"the return type should be float, found {hints.get('return')!r}"


def test_find_user_hints():
    hints = _hints("find_user")
    assert hints.get("users") == dict[str, int], f"users should be dict[str, int], found {hints.get('users')!r}"
    assert hints.get("name") is str, f"name should be str, found {hints.get('name')!r}"
    assert hints.get("return") == (int | None), f"the return type should be int | None, found {hints.get('return')!r}"


def test_apply_twice_hints():
    hints = _hints("apply_twice")
    func = hints.get("func")
    assert typing.get_origin(func) is collections.abc.Callable, f"func should be Callable[[int], int], found {func!r}"
    assert typing.get_args(func) == ([int], int), f"func should take one int and return an int, found {func!r}"
    assert hints.get("value") is int, f"value should be int, found {hints.get('value')!r}"
    assert hints.get("return") is int, f"the return type should be int, found {hints.get('return')!r}"


def test_greet_hints_and_default():
    greet = _fn("greet")
    hints = typing.get_type_hints(greet)
    assert hints.get("name") is str, f"name should be str, found {hints.get('name')!r}"
    assert hints.get("return") is str, f"the return type should be str, found {hints.get('return')!r}"
    assert greet() == "Hello, world!", "keep the default value 'world' for name"


def test_user_typed_dict_and_describe():
    import exercise

    User = _cls("User")
    assert typing.is_typeddict(User), "User should be a class that inherits from TypedDict"
    assert typing.get_type_hints(User) == {"name": str, "age": int}, f"User should have name: str and age: int, found {typing.get_type_hints(User)!r}"
    hints = _hints("describe")
    assert hints.get("user") is User, f"user should be hinted as User, found {hints.get('user')!r}"
    assert hints.get("return") is str, f"the return type should be str, found {hints.get('return')!r}"
    assert exercise.describe({"name": "Ada", "age": 36}) == "Ada is 36", "describe should still work"


def test_functions_still_work():
    average = _fn("average")
    find_user = _fn("find_user")
    apply_twice = _fn("apply_twice")
    assert average([1, 2, 3]) == 2, "average([1, 2, 3]) should still be 2"
    assert find_user({"ann": 3}, "ann") == 3 and find_user({}, "bo") is None, "find_user should still return the value or None"
    assert apply_twice(lambda n: n + 3, 1) == 7, "apply_twice should still apply the function two times"
