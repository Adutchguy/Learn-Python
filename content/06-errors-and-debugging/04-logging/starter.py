# Write three functions:
#
# import logging
#
# def make_logger(name, stream): ...          returns a logger writing "LEVEL: message" lines to stream
# def process_orders(orders, logger): ...     warn about bad quantities, info for good ones, return how many were good
# def safe_parse(text, logger): ...           int(text), or log an error and return None
