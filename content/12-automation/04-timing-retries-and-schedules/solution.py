import time
from datetime import datetime, timedelta


class Stopwatch:
    def __init__(self, clock=time.perf_counter):
        self.clock = clock
        self.begin = None

    def start(self):
        self.begin = self.clock()

    def stop(self):
        return self.clock() - self.begin


def retry(func, attempts, delay, sleep=time.sleep):
    for attempt in range(attempts):
        try:
            return func()
        except Exception:
            if attempt == attempts - 1:
                raise
            sleep(delay)
            delay *= 2


def next_runs(start, every_minutes, count):
    return [start + timedelta(minutes=every_minutes * i) for i in range(count)]


def run_every(task, interval, times, sleep=time.sleep):
    results = []
    for i in range(times):
        if i > 0:
            sleep(interval)
        results.append(task())
    return results
