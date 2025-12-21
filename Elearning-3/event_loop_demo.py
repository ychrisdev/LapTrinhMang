import asyncio
import time

def run_event_loop(n):
    print("\n--- Event-driven / Event Loop ---")
    start = time.time()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def fake_event_task(client_id):
        print(f"[Client {client_id}] Gui request")
        # sau 2 giây thì gọi callback response
        loop.call_later(2, on_response, client_id)

    def on_response(client_id):
        print(f"[Client {client_id}] Nhan response (event)")

    # đăng ký các sự kiện
    for i in range(n):
        fake_event_task(i)

    # chạy event loop trong 3 giây để xử lý event
    loop.run_until_complete(asyncio.sleep(3))
    loop.close()

    print("Time:", round(time.time() - start, 2), "seconds")
