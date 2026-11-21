import time
import asyncio
from concurrent.futures import ProcessPoolExecutor


def fetch_data(param):
    print(f"Do something with {param}...", flush=True)
    time.sleep(param)
    print(f"Done with {param}", flush=True)
    return f"Result of {param}"


async def main():
    # run in thread
    task1 = asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2 = asyncio.create_task(asyncio.to_thread(fetch_data, 2))
    result1 = await task1
    print("Thread 1 fully completed")
    result2 = await task2
    print("Thread 2 fully completed")

    # run in Process Pool
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        task1 = loop.run_in_executor(executor, fetch_data, 1)
        task2 = loop.run_in_executor(executor, fetch_data, 2)
        result1 = await task1
        print("Process 1 fully completed")
        result2 = await task2
        print("Process 2 fully completed")

    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()

print(f"Finished in {t2 - t1:.2f} seconds")

"""
----------------------------------------------------------------------------

                 asyncio event loop
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
         Thread 1              Thread 2
         fetch(1)              fetch(2)
         sleep(1)              sleep(2)
              │                   │
              ▼                   ▼
          complete             complete

----------------------------------------------------------------------------------------

                asyncio event loop
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
         Process 1             Process 2
         fetch(1)              fetch(2)
         sleep(1)              sleep(2)
              │                   │
              ▼                   ▼
          complete             complete


-----------------------------------------------------------------------------

                MAIN / EVENT LOOP
                         │
                         ▼
              ┌─────────────────────┐
              │    THREAD PHASE     │
              │                     │
              │ Thread 1: 1 sec     │
              │ Thread 2: 2 sec     │
              │                     │
              │ Total: ~2 sec       │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   PROCESS PHASE     │
              │                     │
              │ Process 1: 1 sec    │
              │ Process 2: 2 sec    │
              │                     │
              │ Total: ~2 sec       │
              └──────────┬──────────┘
                         │
                         ▼
                    MAIN RETURNS

                  Total ≈ 4 seconds

----------------------------------------------------------------------------------
                  
                         asyncio.run(main())
                                  │
                                  ▼
                        ┌──────────────────┐
                        │   asyncio Event  │
                        │      Loop        │
                        └────────┬─────────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
                  ▼                             ▼
          ┌───────────────┐             ┌────────────────┐
          │  THREAD PHASE │             │ PROCESS PHASE  │
          └───────┬───────┘             └───────┬────────┘
                  │                             │
             ~2 seconds                    ~2 seconds
                  │                             │
                  └──────────────┬──────────────┘
                                 ▼
                              Return
                                 │
                                 ▼
                         Total ≈ 4 seconds

"""
