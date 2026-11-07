import time
from datetime import datetime, timedelta


# Write these (each takes the real clock/sleep as a default so checks can swap in fakes):
#
# class Stopwatch:                              Stopwatch(clock=time.perf_counter); start(); stop() -> seconds
# def retry(func, attempts, delay, sleep=time.sleep): ...     call func until it works; double the delay each failure
# def next_runs(start, every_minutes, count): ...             list of datetimes spaced every_minutes apart
# def run_every(task, interval, times, sleep=time.sleep): ... call task() `times` times, waiting between; return results
