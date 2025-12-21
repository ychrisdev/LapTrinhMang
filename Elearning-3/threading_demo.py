import time
import threading
from task import fake_network_task

def run_threading(n):
    print("\n--- Multithreading ---")
    start = time.time()
    threads = []

    for i in range(n):
        t = threading.Thread(target=fake_network_task, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Time:", round(time.time() - start, 2), "seconds")
