import time
from concurrent.futures import ThreadPoolExecutor
from task import fake_network_task

def run_future(n):
    print("\n---Promise ---")
    start = time.time()

    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(fake_network_task, i) for i in range(n)]
        for f in futures:
            f.result()

    print("Time:", round(time.time() - start, 2), "seconds")
