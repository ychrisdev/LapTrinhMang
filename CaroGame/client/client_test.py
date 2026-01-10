# client/client_test.py
import socket
import json

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("1. Create room 3x3")
print("2. Create room 10x10")
print("3. Join room")

choice = input("Choose: ")

if choice == "1":
    msg = {"type": "create_room", "data": {"size": 3}}
elif choice == "2":
    msg = {"type": "create_room", "data": {"size": 10}}
else:
    msg = {"type": "join_room", "data": {}}

client.sendall(json.dumps(msg).encode())

while True:
    data = client.recv(1024)
    if not data:
        break
    print("Server:", data.decode())
