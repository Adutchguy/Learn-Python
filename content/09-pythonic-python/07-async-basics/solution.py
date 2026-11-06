import asyncio


async def fetch(name, delay):
    await asyncio.sleep(delay)
    return f"{name} done"


async def fetch_all(jobs):
    coroutines = [fetch(name, delay) for name, delay in jobs]
    return await asyncio.gather(*coroutines)


def run_all(jobs):
    return asyncio.run(fetch_all(jobs))
