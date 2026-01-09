import socket
import json
from config import HOST, PORT, BUFFER_SIZE

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print("Da ket noi toi server.")
        print("Nhap keo / bua / bao | 'thoat' de thoat\n")

        while True:
            choice = input("Lua chon cua ban: ").strip().lower()
            client_socket.send(choice.encode())

            if choice == "thoat":
                print(client_socket.recv(BUFFER_SIZE).decode())
                break

            result = json.loads(client_socket.recv(BUFFER_SIZE).decode())

            if result["status"] == "ok":
                print("Ban chon        :", result["lua_chon_client"])
                print("Server chon     :", result["lua_chon_server"])
                print("Ket qua         :", result["ket_qua"])
                print(
                    f"Ti so           : Client {result['client_score']} - "
                    f"{result['server_score']} Server"
                )
                print("-" * 30)
            else:
                print("Loi:", result["message"])

    finally:
        client_socket.close()
        print("Da dong ket noi.")


if __name__ == "__main__":
    start_client()
