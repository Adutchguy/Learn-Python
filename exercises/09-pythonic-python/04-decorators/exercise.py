import functools

# Write two decorators:
#
# count_calls(func)   -> wrapper with a `calls` attribute
# retry(times)        -> decorator factory that tries up to `times` times
