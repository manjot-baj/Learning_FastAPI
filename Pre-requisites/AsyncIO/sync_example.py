import time


def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


def main():
    result1 = fetch_data(1)
    print("Fetch 1 fully completed")
    result2 = fetch_data(2)
    print("Fetch 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = main()
print(results)

t2 = time.perf_counter()

print(f"Finished in {t2 - t1:.2f} seconds")

# main() executes the fetch data func syncronously one by one,
# after complete execution of result1 = fetch_data(1), result2 is called and executed

"""

main()
 │
 ├── result1 = fetch_data(1)
 │       │
 │       ├── print
 │       ├── time.sleep(1)  ← main waits here
 │       ├── print
 │       └── return result1
 │
 ├── print("Fetch 1 fully completed")
 │
 ├── result2 = fetch_data(2)
 │       │
 │       ├── print
 │       ├── time.sleep(2)  ← main waits here
 │       ├── print
 │       └── return result2
 │
 └── print("Fetch 2 fully completed")

"""
