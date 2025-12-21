import time
import threading

def fake_task_callback(client_id, callback):
    print(f"[Client {client_id}] Gui request")
    time.sleep(2)
    callback(client_id)

def on_response(client_id):
    print(f"[Client {client_id}] Nhan response (callback)")

def run_callback(n):
    print("\n--- Callback ---")
    start = time.time()

    for i in range(n):
        threading.Thread(
            target=fake_task_callback,
            args=(i, on_response)
        ).start()

    time.sleep(3)
    print("Time:", round(time.time() - start, 2), "seconds")
