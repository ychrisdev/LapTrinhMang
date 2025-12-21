import asyncio
import time

async def async_task(client_id):
    print(f"[Client {client_id}] Gui request")
    await asyncio.sleep(2)
    print(f"[Client {client_id}] Nhan response")

async def run_async_tasks(n):
    tasks = [async_task(i) for i in range(n)]
    await asyncio.gather(*tasks)

def run_async_await(n):
    print("\n--- Async / Await ---")
    start = time.time()
    asyncio.run(run_async_tasks(n))
    print("Time:", round(time.time() - start, 2), "seconds")
