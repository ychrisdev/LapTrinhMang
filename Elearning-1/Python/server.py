import socket
import sys

# Hiển thị tiếng Việt trên Windows
sys.stdout.reconfigure(encoding='utf-8')

HOST = "0.0.0.0"
PORT = 8888

# Tạo socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# --- TỐI ƯU TCP ---
# Cho phép bind lại cổng
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Tắt Nagle (gửi ngay)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# Bật TCP Keep-Alive
server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# --- Khởi động server ---
server.bind((HOST, PORT))
server.listen(5)

print(f"Server đang lắng nghe tại {HOST}:{PORT} ...")

while True:
    conn, addr = server.accept()
    print("Kết nối từ:", addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break

        message = data.decode().strip()
        print("Nhận từ client:", message)

        response = "Server da nhan!\n"
        conn.sendall(response.encode())

    conn.close()
    print("Client đã đóng kết nối.\n")
