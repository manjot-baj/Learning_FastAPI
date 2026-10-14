import time
import asyncio


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
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

# asyncio.run(main()) triggers a event loop where the task1 and task2 are ready concurrently to execute
# event loop is running in single thread and process.
# Inside Event Loop
# main()(Running), task1(Ready), task2(Ready)
# when task1 await, main()(Suspend), task1(Running), task2(Ready)
# when task1 --> await asyncio.sleep(1), main()(Suspend), task1(Suspend)(executing Background), task2(Running)
# when task2 --> await asyncio.sleep(2), main()(Suspend), task1(completed)(prints the result), task2(Suspend)(executing Background)
# Completed execution when task2(completed)

"""

asyncio.run(main())
        │
        ▼
    Event Loop
        │
        ├── main()
        │
        ├── task1 → fetch_data(1)
        │
        └── task2 → fetch_data(2)


main() → await task1
             │
             ▼
       main() suspended
             │
             ├── task1 runs
             │     prints "Do something with 1..."
             │     await sleep(1)
             │     └── task1 suspended
             │
             └── task2 runs
                   prints "Do something with 2..."
                   await sleep(2)
                   └── task2 suspended


After ~1 second:
    task1 wakes up
        │
        ├── prints "Done with 1"
        └── completes

main() resumes
    │
    └── prints "Task 1 fully completed"

main() → await task2
             │
             ▼
        task2 is still sleeping
             │
             │ ~1 more second
             ▼
        task2 wakes up
             │
             ├── prints "Done with 2"
             └── completes

main() resumes
    │
    └── prints "Task 2 fully completed"

"""
