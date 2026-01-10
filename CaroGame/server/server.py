# server/server.py
import socket
import threading
from protocol import decode, encode
from room import Room
from game_logic import check_win, check_draw

HOST = "0.0.0.0"
PORT = 5000

rooms = []
waiting_room = None


def handle_client(conn, addr):
    global waiting_room
    print(f"[+] Client connected: {addr}")

    current_room = None  # Room mà client này thuộc về

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = decode(data)
            print(f"[{addr}] -> {msg}")

            msg_type = msg["type"]
            payload = msg["data"]

            if msg_type == "create_room":
                size = payload["size"]
                room = Room(size)
                room.add_player(conn)
                rooms.append(room)
                waiting_room = room
                current_room = room

                conn.sendall(encode("room_created", {"size": size}))
                print(f"Room created with size {size}")

            elif msg_type == "join_room":
                if waiting_room and not waiting_room.is_full():
                    waiting_room.add_player(conn)
                    current_room = waiting_room

                    p1, p2 = waiting_room.players
                    p1.sendall(encode("start_game", {
                        "size": waiting_room.size,
                        "symbol": "X",
                        "your_turn": True
                    }))
                    p2.sendall(encode("start_game", {
                        "size": waiting_room.size,
                        "symbol": "O",
                        "your_turn": False
                    }))

                    print("Room full -> game started")
                    waiting_room = None
                else:
                    conn.sendall(encode("error", {
                        "message": "No available room"
                    }))

            elif msg_type == "move":
                if not current_room or current_room.finished:
                    continue

                if conn != current_room.current_player():
                    conn.sendall(encode("error", {
                        "message": "Not your turn"
                    }))
                    continue

                x = payload["x"]
                y = payload["y"]
                symbol = current_room.get_symbol(conn)

                if current_room.board[x][y] is not None:
                    conn.sendall(encode("error", {
                        "message": "Cell occupied"
                    }))
                    continue

                current_room.board[x][y] = symbol

                for p in current_room.players:
                    p.sendall(encode("update", {
                        "x": x,
                        "y": y,
                        "symbol": symbol
                    }))

                if check_win(current_room.board, x, y, symbol):
                    for p in current_room.players:
                        p.sendall(encode("win", {
                            "winner": symbol
                        }))
                    current_room.finished = True
                    continue

                if check_draw(current_room.board):
                    for p in current_room.players:
                        p.sendall(encode("draw", {}))
                    current_room.finished = True
                    continue

                current_room.switch_turn()

            elif msg_type == "rematch":
                if current_room and current_room.finished:
                    current_room.reset()
                    p1, p2 = current_room.players

                    p1.sendall(encode("start_game", {
                        "size": current_room.size,
                        "symbol": "X",
                        "your_turn": True
                    }))
                    p2.sendall(encode("start_game", {
                        "size": current_room.size,
                        "symbol": "O",
                        "your_turn": False
                    }))

            elif msg_type == "leave_room":
                if current_room:
                    for p in current_room.players:
                        if p != conn:
                            p.sendall(encode("back_to_menu", {
                                "message": "Opponent left"
                            }))

                    if current_room in rooms:
                        rooms.remove(current_room)

                    if waiting_room == current_room:
                        waiting_room = None

                    current_room = None
                    conn.sendall(encode("back_to_menu", {}))

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")

    finally:
        print(f"[-] Client disconnected: {addr}")

        if current_room:
            if current_room in rooms:
                rooms.remove(current_room)

            # Nếu room đó đang là waiting_room thì xóa luôn
            if waiting_room == current_room:
                waiting_room = None

        conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    main()
