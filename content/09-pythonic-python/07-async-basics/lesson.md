---
title: "async and await: Doing Waiting Work Together"
minutes: 20
prereqs: ["09-pythonic-python/06-type-hints"]
concepts: ["asyncio", "async def", "await", "asyncio.gather", "concurrency", "event loop"]
local_only: true
hints:
  - "fetch is an async def. Inside it: await asyncio.sleep(delay), then return f\"{name} done\". The await is where the function pauses and lets other tasks run."
  - "fetch_all(jobs) is also async def. Build one coroutine per job with a list comprehension: [fetch(name, delay) for name, delay in jobs]. Then return await asyncio.gather(*coroutines), which runs them together and returns results in the same order."
  - "run_all(jobs) is a normal function: return asyncio.run(fetch_all(jobs)). asyncio.run starts the event loop, runs the coroutine to the end and returns its result."
---

## Why this matters

Many programs spend most of their time **waiting**: for a web page, a database or a file. `async` code lets one program start several waiting jobs at once, instead of finishing one before beginning the next. It does not make calculations faster; it makes waiting overlap.

## The idea

A function defined with `async def` is a **coroutine function**: calling it does not run it, it creates a coroutine. `await` marks a point where it can pause while something slow happens, so other coroutines can run meanwhile. The **event loop** runs them, and `asyncio.run()` starts it:

```python
import asyncio

async def say(word, delay):
    await asyncio.sleep(delay)        # pause without blocking anyone else
    return word

async def main():
    results = await asyncio.gather(   # run all three together
        say("a", 0.3),
        say("b", 0.3),
        say("c", 0.3),
    )
    print(results)                    # ['a', 'b', 'c'] after 0.3 s, not 0.9 s

asyncio.run(main())
```

`asyncio.gather` returns the results in the order you passed the coroutines, not the order they finished.

Rules to remember:

- `await` only works inside an `async def`.
- A coroutine that is never awaited never runs (Python warns you).
- `time.sleep()` blocks everything; use `await asyncio.sleep()` in async code.
- Async helps with waiting (network, files, timers). For heavy calculation, it does not help.

## Try it

This lesson runs on your own computer (`asyncio.run` needs a real event loop, which the in-browser Python cannot start). Change the delays in the example and watch the total time.

## Your turn

Write:

- `async def fetch(name, delay)`: wait `delay` seconds with `asyncio.sleep`, then return `"<name> done"`.
- `async def fetch_all(jobs)`: `jobs` is a list of `(name, delay)` pairs. Run all the fetches **at the same time** and return the list of results in the same order.
- `def run_all(jobs)`: an ordinary function that runs `fetch_all(jobs)` with `asyncio.run` and returns the result.

The check makes sure three half-second jobs finish together in about half a second, not one after another.

## Recap

- `async def` makes a coroutine function; `await` pauses it while waiting.
- `asyncio.run(coro)` starts the event loop and runs `coro`.
- `asyncio.gather(*coros)` runs coroutines together and keeps their order.
- Async is for waiting work; it is not a way to speed up calculations.

## Common mistakes

- **Calling a coroutine without `await`**, so it never runs.
- **Using `time.sleep`** inside async code, which freezes every task.
- **Awaiting one job at a time in a loop**, which runs them one after another.
