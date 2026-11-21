import time
import asyncio


async def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result1 = await task1
    print("Task 1 fully completed")
    result2 = await task2
    print("Task 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()

print(f"Finished in {t2 - t1:.2f} seconds")

# sync code inside async blocks the event loop

"""

asyncio.run(main())
        │
        ▼
    Event Loop
        │
        ▼
main()
        │
        ├── create task1
        ├── create task2
        │
        ▼
await task1
        │
        ▼
task1 starts
        │
        ├── print("Do something with 1...")
        │
        ├── time.sleep(1)  ← BLOCKS EVENT LOOP
        │
        └── print("Done with 1")
        │
        ▼
task1 completes
        │
        ▼
main() resumes
        │
        ├── "Task 1 fully completed"
        │
        ▼
await task2
        │
        ▼
task2 starts
        │
        ├── print("Do something with 2...")
        │
        ├── time.sleep(2)  ← BLOCKS EVENT LOOP
        │
        └── print("Done with 2")
        │
        ▼
task2 completes

"""
