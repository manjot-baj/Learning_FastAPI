import time
import asyncio


# coroutine
async def fetch_data(param):
    await asyncio.sleep(param)
    return f"Result of {param}"


async def main():
    # Tasks
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result1 = await task1
    result2 = await task2
    print(f"Tasks results: {[result1, result2]}")

    # Gather Coroutine
    coroutines = [fetch_data(i) for i in range(1, 3)]
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    print(f"Gathered Coroutine results: {results}")

    # Gather Tasks
    tasks = [asyncio.create_task(fetch_data(i)) for i in range(1, 3)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"Gathered Tasks results: {results}")

    # Task Group
    async with asyncio.TaskGroup() as tg:
        # All tasks are awaited when context manager exits.
        results = [tg.create_task(fetch_data(i)) for i in range(1, 3)]
    print(f"Task Group Results: {[result.result() for result in results]}")

    return "Main Coroutine Done"


t1 = time.perf_counter()

# event loop
results = asyncio.run(main())
print(results)

t2 = time.perf_counter()

print(f"Finished in {t2 - t1:.2f} seconds")


"""

                         asyncio.run(main())
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Event Loop    │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │ 1. create_task()         │
                    │                          │
                    │ task1 ── sleep(1)        │
                    │ task2 ── sleep(2)        │
                    │                          │
                    │          ≈ 2 sec         │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ 2. gather(coroutines)    │
                    │                          │
                    │ coro1 ── sleep(1)        │
                    │ coro2 ── sleep(2)        │
                    │                          │
                    │          ≈ 2 sec         │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ 3. gather(Tasks)         │
                    │                          │
                    │ task1 ── sleep(1)        │
                    │ task2 ── sleep(2)        │
                    │                          │
                    │          ≈ 2 sec         │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ 4. TaskGroup             │
                    │                          │
                    │ task1 ── sleep(1)        │
                    │ task2 ── sleep(2)        │
                    │                          │
                    │          ≈ 2 sec         │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                         Main Coroutine Done

"""
