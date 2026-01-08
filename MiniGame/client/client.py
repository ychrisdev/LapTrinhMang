import socket
import json

from config import HOST, PORT, BUFFER_SIZE

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print("Da ket noi toi server.")
        print("Nhap keo / bua / bao de choi")
        print("Nhap 'thoat' de ket thuc\n")

        while True:
            choice = input("Lua chon cua ban: ").strip().lower()

            client_socket.send(choice.encode())

            # Neu nguoi choi chon thoat
            if choice == "thoat":
                message = client_socket.recv(BUFFER_SIZE).decode()
                print(message)
                break

            response = client_socket.recv(BUFFER_SIZE).decode()
            result = json.loads(response)

            if result["status"] == "ok":
                print("Lua chon cua ban   :", result["lua_chon_client"])
                print("Lua chon cua server:", result["lua_chon_server"])
                print("Ket qua            :", result["ket_qua"])
                print("-" * 30)
            else:
                print("Loi:", result["message"])

    except Exception as e:
        print("Khong the ket noi toi server:", e)

    finally:
        client_socket.close()
        print("Da dong ket noi.")


if __name__ == "__main__":
    start_client()
