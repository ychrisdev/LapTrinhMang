import socket
import time
import sys

# Hiển thị tiếng Việt trên Windows
sys.stdout.reconfigure(encoding='utf-8')

HOST = "127.0.0.1"
PORT = 8888

# Tạo socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# --- TỐI ƯU TCP ---
# Tắt Nagle
client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# Bật TCP Keep-Alive
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# --- Kết nối tới server ---
print("Đang kết nối tới server...")
client.connect((HOST, PORT))
print("Đã kết nối!\n")

# Gửi dữ liệu
for i in range(5):
    msg = f"Goi tin thu {i}"
    print("Gửi:", msg)

    client.sendall((msg + "\n").encode())
    data = client.recv(1024)

    print("Server trả về:", data.decode().strip())
    time.sleep(0.2)

# Đóng kết nối
client.close()
print("\nĐã đóng kết nối.")
