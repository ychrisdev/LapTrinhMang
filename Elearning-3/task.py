import time

def fake_network_task(client_id, delay=2):
    print(f"[Client {client_id}] Gui request")
    time.sleep(delay)
    print(f"[Client {client_id}] Nhan response")
