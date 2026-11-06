import logging


def make_logger(name, stream):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def process_orders(orders, logger):
    good = 0
    for order in orders:
        if order["qty"] <= 0:
            logger.warning(f"order {order['id']}: bad quantity {order['qty']}")
        else:
            logger.info(f"order {order['id']}: ok")
            good += 1
    return good


def safe_parse(text, logger):
    try:
        return int(text)
    except ValueError:
        logger.error(f"could not parse {text!r}")
        return None
