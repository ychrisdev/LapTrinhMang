import time
from task import fake_network_task

def run_sequential(n):
    print("\n--- Sequential ---")
    start = time.time()

    for i in range(n):
        fake_network_task(i)

    print("Time:", round(time.time() - start, 2), "seconds")
