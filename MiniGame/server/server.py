import socket
import threading
import json

from config import HOST, PORT, BUFFER_SIZE
from logic import play_game


def handle_client(conn, addr):
    print(f"[KET NOI MOI] {addr}")

    client_score = 0
    server_score = 0

    try:
        while True:
            data = conn.recv(BUFFER_SIZE).decode()
            if not data:
                break

            data = data.strip().lower()
            print(f"[DU LIEU NHAN] {addr}: {data}")

            if data == "thoat":
                conn.send("Da thoat khoi tro choi.".encode())
                break

            result = play_game(data)

            if result["status"] == "ok":
                if result["ket_qua"] == "thang":
                    client_score += 1
                elif result["ket_qua"] == "thua":
                    server_score += 1

                result["client_score"] = client_score
                result["server_score"] = server_score

            response = json.dumps(result, ensure_ascii=False)
            conn.send(response.encode())

    except Exception as e:
        print(f"[LOI] {addr}: {e}")

    finally:
        conn.close()
        print(f"[NGAT KET NOI] {addr}")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[SERVER DANG CHAY] {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(
            target=handle_client,
            args=(conn, addr)
        ).start()


if __name__ == "__main__":
    start_server()
