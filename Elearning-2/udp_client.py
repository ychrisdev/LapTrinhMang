# udp_client.py
import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

sequence = 1

BATCH_SIZE = 3        # Batching
RATE_LIMIT = 0.5     # Rate Control (giây)
MAX_PACKET_SIZE = 1200  # Packet Size Optimization

def send_packet(seq, ptype, fec, payload):
    msg = f"{seq}|{ptype}|{fec}|{payload}"

    # Packet Size Optimization
    if len(msg.encode()) > MAX_PACKET_SIZE:
        print("Packet too large → split (demo)")
        return

    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))
    print(f" Sent seq={seq}, type={ptype}, data={payload}")

    # ACK + Retransmission
    if ptype == "IMPORTANT":
        try:
            ack, _ = sock.recvfrom(1024)
            print(f"Received {ack.decode()}")
        except socket.timeout:
            print(" ACK timeout → Retransmission")
            sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))

# ---------- BATCHING ----------
batch = []
for i in range(6):
    batch.append(f"msg{i}")

    if len(batch) == BATCH_SIZE:
        data = ",".join(batch)
        send_packet(sequence, "NORMAL", "NO", data)
        sequence += 1
        batch.clear()
        time.sleep(RATE_LIMIT)

# ---------- SELECTIVE RELIABILITY ----------
send_packet(sequence, "IMPORTANT", "NO", "critical_data")
sequence += 1
time.sleep(RATE_LIMIT)

# ---------- FEC DEMO ----------
data1 = "10"
data2 = "20"
parity = str(int(data1) ^ int(data2))

send_packet(sequence, "NORMAL", "DATA", data1)
sequence += 1

send_packet(sequence, "NORMAL", "DATA", data2)
sequence += 1

send_packet(sequence, "NORMAL", "PARITY", parity)
sequence += 1
