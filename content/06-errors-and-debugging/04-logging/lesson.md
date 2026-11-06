---
title: "Logging Instead of print"
minutes: 18
prereqs: ["06-errors-and-debugging/03-debugging-strategies"]
concepts: ["logging", "log levels", "logger", "handler", "formatter", "StreamHandler"]
local_only: false
hints:
  - "make_logger: logger = logging.getLogger(name); logger.setLevel(logging.INFO); logger.handlers.clear() so calling it twice does not duplicate lines; add logging.StreamHandler(stream) with handler.setFormatter(logging.Formatter(\"%(levelname)s: %(message)s\")); set logger.propagate = False; return logger."
  - "process_orders: loop over the orders. If order[\"qty\"] <= 0 call logger.warning(f\"order {order['id']}: bad quantity {order['qty']}\"); otherwise call logger.info(f\"order {order['id']}: ok\") and count it. Return the count of good orders."
  - "safe_parse: try: return int(text) except ValueError: call logger.error(f\"could not parse {text!r}\") and return None."
---

## Why this matters

`print` is fine for a learner's first program. Real programs use **logging**: messages come with a severity level, can be switched on or off without editing code, and can go to the screen, a file or a service.

## The idea

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("shop")

log.debug("cart contents: [...]")      # hidden: below INFO
log.info("order 7 accepted")           # INFO: order 7 accepted
log.warning("stock is low")            # WARNING: stock is low
log.error("payment failed")            # ERROR: payment failed
```

Levels, from quiet to loud: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. A logger shows messages at or above its level.

Under the hood a **logger** creates messages, a **handler** decides where they go (`StreamHandler(stream)` writes to a stream) and a **formatter** decides how they look. Inside an `except` block, `log.exception("...")` also records the traceback.

## Try it

Change `level=logging.INFO` to `logging.DEBUG`, then to `logging.ERROR`. Which messages appear each time?

## Your turn

Write three functions:

- `make_logger(name, stream)`: return the logger called `name`, at level `INFO`, with **one** handler that writes to `stream` in the format `LEVEL: message` (`"%(levelname)s: %(message)s"`). Set `logger.propagate = False` so the root logger does not print it a second time. Calling the function again with the same name must replace the old handler, not add a second one.
- `process_orders(orders, logger)`: each order is a dictionary like `{"id": 3, "qty": 2}`. A quantity of 0 or less logs a warning `order 3: bad quantity 0`; otherwise log an info message `order 3: ok`. Return how many orders were fine.
- `safe_parse(text, logger)`: return `int(text)`; if the text is not a whole number, log an error `could not parse 'abc'` (with `!r`) and return `None`.

## Recap

- Use logging levels instead of `print` so output can be filtered and redirected.
- A logger makes messages, a handler picks the destination, a formatter picks the look.
- `log.exception(...)` inside `except` records the traceback too.

## Common mistakes

- **Doing nothing and expecting INFO to appear.** The default level is `WARNING`; set a level.
- **Adding a handler every time a function runs**, so each message prints several times.
- **Logging secrets** such as passwords or tokens.
