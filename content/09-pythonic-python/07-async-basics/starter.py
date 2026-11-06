import asyncio

# Write:
#   async def fetch(name, delay)   -> wait, then return "<name> done"
#   async def fetch_all(jobs)      -> run all jobs together, results in order
#   def run_all(jobs)              -> asyncio.run(fetch_all(jobs))
