import socket
import threading
import json

from config import HOST, PORT, BUFFER_SIZE
from logic import play_game


def handle_client(conn, addr):
    print(f"[KET NOI MOI] {addr}")

    try:
        while True:
            data = conn.recv(BUFFER_SIZE).decode()

            # Client ngat ket noi dot ngot
            if not data:
                break

            data = data.strip().lower()
            print(f"[DU LIEU NHAN] {addr}: {data}")

            # Neu client chon thoat
            if data == "thoat":
                conn.send("Da thoat khoi tro choi.".encode())
                break

            # Xu ly game
            result = play_game(data)

            response = json.dumps(result, ensure_ascii=False)
            conn.send(response.encode())

    except Exception as e:
        print(f"[LOI] {addr}: {e}")

    finally:
        conn.close()
        print(f"[NGAT KET NOI] {addr}")


def start_server():
    """
    Ham khoi dong server
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[SERVER DANG CHAY] {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()

        # Tao thread moi cho moi client
        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )
        client_thread.start()


if __name__ == "__main__":
    start_server()
