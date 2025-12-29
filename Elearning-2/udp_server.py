# udp_server.py
import socket
import random

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print("UDP Server running...")

received_packets = {}

while True:
    data, addr = sock.recvfrom(4096)
    msg = data.decode()

    # Giả lập mất gói 20%
    if random.random() < 0.2:
        print("Packet lost (simulated)")
        continue

    # Format:
    # seq|type|fec|payload
    seq, ptype, fec, payload = msg.split("|")

    seq = int(seq)
    print(f"Received seq={seq}, type={ptype}, data={payload}")

    received_packets[seq] = payload

    # ACK giả lập + Selective Reliability
    if ptype == "IMPORTANT":
        ack = f"ACK|{seq}"
        sock.sendto(ack.encode(), addr)
        print(f"Sent ACK for seq={seq}")

    # FEC demo (chỉ minh họa)
    if fec == "PARITY":
        print("FEC parity received (demo)")
