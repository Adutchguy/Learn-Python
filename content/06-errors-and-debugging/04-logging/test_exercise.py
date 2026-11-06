def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _test_logger(name):
    """A logger the checks control themselves, so each check is independent of your make_logger."""
    import io
    import logging

    stream = io.StringIO()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger, stream


def test_make_logger_writes_levels_at_info_and_above():
    import io

    make_logger = _fn("make_logger")
    stream = io.StringIO()
    logger = make_logger("check-levels", stream)
    logger.debug("hidden")
    logger.info("hi")
    logger.warning("careful")
    assert stream.getvalue() == "INFO: hi\nWARNING: careful\n", (
        f"The stream should hold 'INFO: hi' and 'WARNING: careful' (debug is below INFO) but holds {stream.getvalue()!r}."
    )


def test_make_logger_returns_the_named_logger():
    import io
    import logging

    make_logger = _fn("make_logger")
    logger = make_logger("check-name", io.StringIO())
    assert isinstance(logger, logging.Logger), f"make_logger should return a logging.Logger but returned {logger!r}."
    assert logger.name == "check-name", f"The logger should be called 'check-name' but is {logger.name!r}."
    assert logger.propagate is False, "Set logger.propagate = False so messages are not also printed by the root logger."


def test_make_logger_replaces_the_old_handler():
    import io

    make_logger = _fn("make_logger")
    first, second = io.StringIO(), io.StringIO()
    make_logger("check-twice", first)
    logger = make_logger("check-twice", second)
    logger.info("x")
    assert second.getvalue() == "INFO: x\n", f"The new stream should hold 'INFO: x' but holds {second.getvalue()!r}."
    assert first.getvalue() == "", f"The old stream should get nothing, but holds {first.getvalue()!r}. Clear logger.handlers before adding the new handler."


def test_process_orders_logs_and_counts():
    process_orders = _fn("process_orders")
    logger, stream = _test_logger("check-orders")
    orders = [{"id": 1, "qty": 2}, {"id": 2, "qty": 0}, {"id": 3, "qty": -1}]
    count = process_orders(orders, logger)
    assert count == 1, f"process_orders should return 1 (only order 1 is fine) but returned {count!r}."
    expected = "INFO: order 1: ok\nWARNING: order 2: bad quantity 0\nWARNING: order 3: bad quantity -1\n"
    assert stream.getvalue() == expected, f"The log should be:\n{expected}\nbut it was:\n{stream.getvalue()}"


def test_process_orders_with_no_orders():
    process_orders = _fn("process_orders")
    logger, stream = _test_logger("check-no-orders")
    assert process_orders([], logger) == 0, "No orders means 0 good orders."
    assert stream.getvalue() == "", "No orders should log nothing."


def test_safe_parse_good_text_logs_nothing():
    safe_parse = _fn("safe_parse")
    logger, stream = _test_logger("check-parse-ok")
    assert safe_parse("12", logger) == 12, "safe_parse('12', logger) should return 12."
    assert stream.getvalue() == "", f"Nothing should be logged for good text but the log holds {stream.getvalue()!r}."


def test_safe_parse_bad_text_logs_an_error():
    safe_parse = _fn("safe_parse")
    logger, stream = _test_logger("check-parse-bad")
    result = safe_parse("abc", logger)
    assert result is None, f"safe_parse('abc', logger) should return None but returned {result!r}."
    assert stream.getvalue() == "ERROR: could not parse 'abc'\n", f"The log should be \"ERROR: could not parse 'abc'\" but it was {stream.getvalue()!r}."
