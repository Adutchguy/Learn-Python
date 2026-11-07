---
title: "Timing, Retrying and Scheduling"
minutes: 24
prereqs: ["07-modules-and-tooling/03-dates-and-times"]
concepts: ["time.sleep", "perf_counter", "retry", "exponential backoff", "timedelta", "dependency injection", "cron"]
local_only: false
hints:
  - "Stopwatch: store the clock function in __init__ (self.clock = clock). start() saves self.begin = self.clock(). stop() returns self.clock() - self.begin. Using self.clock rather than time.perf_counter directly is what lets the checks use a fake clock."
  - "retry: loop attempt in range(attempts); try: return func(). On an exception, if it was the last attempt re-raise it (raise), otherwise call sleep(delay) and double the delay for the next time. The error to catch is Exception."
  - "next_runs: [start + timedelta(minutes=every_minutes * i) for i in range(count)]. run_every: call task() times times, and call sleep(interval) only BETWEEN calls, so not after the last one. Collect and return the list of results."
---

## Why this matters

Automation scripts live in a messy world: networks drop, servers are busy, and jobs must run at set times. Four small ideas cover most of it: **timing** how long something takes, **waiting** (`sleep`), **retrying** when something fails, and **scheduling** work to repeat.

## The idea

```python
import time

start = time.perf_counter()        # a precise clock for measuring durations
do_something()
print(time.perf_counter() - start, "seconds")

time.sleep(2)                      # pause the program for 2 seconds
```

**Retrying with backoff.** A flaky operation often works if you simply try again, a little later each time:

```python
def retry(func, attempts, delay):
    for attempt in range(attempts):
        try:
            return func()
        except Exception:
            if attempt == attempts - 1:
                raise                  # out of attempts: let the error out
            time.sleep(delay)
            delay *= 2                 # wait longer each time ("exponential backoff")
```

**Testing code that waits.** A test that really sleeps for 30 seconds is useless. Instead, **pass the clock and the sleep function in as parameters**, with the real ones as defaults:

```python
def retry(func, attempts, delay, sleep=time.sleep): ...
```

In normal use nothing changes. In a check you hand in a fake `sleep` that just records the delays, so the test runs instantly and can check them. This is called **dependency injection**, and it is how you test anything involving time.

**Schedules.** Arithmetic with `datetime` and `timedelta` computes when jobs should run:

```python
from datetime import datetime, timedelta
first = datetime(2026, 1, 1, 9, 0)
[first + timedelta(minutes=30 * i) for i in range(3)]   # 9:00, 9:30, 10:00
```

For jobs that must run when your program is not running, use the operating system's scheduler instead (`cron` on Linux and macOS, Task Scheduler on Windows) and let it start your script.

## Try it

Time a loop that adds up `range(1_000_000)` with `perf_counter`. Then write a function that raises an error the first two times it is called and succeeds on the third, and call it through the `retry` above.

## Your turn

Every function that waits takes a `sleep` (and the stopwatch a `clock`) so it can be checked quickly.

- `Stopwatch(clock=time.perf_counter)`: a class with `start()` and `stop()`; `stop()` returns the seconds since `start()`.
- `retry(func, attempts, delay, sleep=time.sleep)`: call `func()` until it succeeds and return its result. After a failure wait `delay` seconds, doubling the delay each time. If every attempt fails, raise the last error. Do not sleep after the final failure.
- `next_runs(start, every_minutes, count)`: a list of `count` datetimes, beginning at `start`, spaced `every_minutes` apart.
- `run_every(task, interval, times, sleep=time.sleep)`: call `task()` `times` times, waiting `interval` seconds between calls (not after the last), and return the list of results.

## Recap

- `perf_counter()` measures durations; `sleep()` pauses.
- Retry with a growing delay, and give up after a fixed number of attempts, re-raising the error.
- Pass `sleep` and `clock` in as parameters so tests do not have to wait.
- `datetime + timedelta` computes schedules; use `cron` or Task Scheduler for jobs outside your program.

## Common mistakes

- **Retrying forever.** Always cap the attempts.
- **Catching an error and hiding it** after the last attempt; re-raise it so the caller knows.
- **Hard-wiring `time.sleep`** into a function, which makes it slow and hard to check.
