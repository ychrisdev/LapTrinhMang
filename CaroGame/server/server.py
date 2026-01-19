import socket
import threading
from protocol import decode, encode
from room import Room
from game_logic import check_win, check_draw

HOST = "0.0.0.0"
PORT = 5000

rooms = []

waiting = {
    3: None,
    10: None
}


def handle_client(conn, addr):
    print(f"[+] Client connected: {addr}")

    current_room = None
    current_size = None

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = decode(data)
            print(f"[{addr}] -> {msg}")

            msg_type = msg["type"]
            payload = msg["data"]

            if msg_type == "quick_play":
                size = payload["size"]
                current_size = size

                if size not in waiting:
                    waiting[size] = None

                if waiting[size] is None:
                    room = Room(size)
                    room.add_player(conn)
                    rooms.append(room)
                    waiting[size] = room
                    current_room = room

                    conn.sendall(encode("waiting", {
                        "message": f"Đang chờ đối thủ ({size}x{size})..."
                    }))
                else:
                    room = waiting[size]
                    room.add_player(conn)
                    current_room = room

                    p1, p2 = room.players
                    p1.sendall(encode("start_game", {
                        "size": size,
                        "symbol": "X",
                        "your_turn": True
                    }))
                    p2.sendall(encode("start_game", {
                        "size": size,
                        "symbol": "O",
                        "your_turn": False
                    }))

                    waiting[size] = None

            elif msg_type == "pause":
                if current_room:
                    current_room.paused_by.add(conn)
                    for p in current_room.players:
                        p.sendall(encode("opponent_pause", {}))

            elif msg_type == "resume":
                if current_room and conn in current_room.paused_by:
                    current_room.paused_by.remove(conn)

                    if not current_room.is_paused():
                        for p in current_room.players:
                            p.sendall(encode("opponent_resume", {}))

            elif msg_type == "move":
                if not current_room or current_room.finished:
                    continue

                # Nếu phòng đang pause → chặn tuyệt đối
                if current_room.is_paused():
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
                    current_room.reset_votes()
                    continue

                if check_draw(current_room.board):
                    for p in current_room.players:
                        p.sendall(encode("draw", {}))

                    current_room.finished = True
                    current_room.reset_votes()
                    continue

                current_room.switch_turn()

            elif msg_type == "rematch":
                if current_room and current_room.finished:
                    current_room.rematch_votes[conn] = True

                    # Nếu đối thủ đã chọn NO → báo cho người này và dọn phòng
                    if any(v is False for v in current_room.rematch_votes.values()):
                        try:
                            conn.sendall(encode("opponent_left", {}))
                        except:
                            pass

                        if current_room in rooms:
                            rooms.remove(current_room)
                        if current_size and waiting.get(current_size) == current_room:
                            waiting[current_size] = None

                        current_room.players.clear()
                        current_room = None
                        return

                    # Nếu cả 2 đều Yes → chơi lại
                    if all(v is True for v in current_room.rematch_votes.values()):
                        current_room.reset()
                        current_room.reset_votes()

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
                if not current_room:
                    continue

                # ===== ĐANG Ở GIAI ĐOẠN REMATCH =====
                if current_room.finished:
                    current_room.rematch_votes[conn] = False

                    # Người bấm NO → về menu ngay
                    try:
                        conn.sendall(encode("back_to_menu", {}))
                    except:
                        pass

                    # Nếu đối thủ chưa chọn gì → KHÔNG làm gì thêm
                    if any(v is None for v in current_room.rematch_votes.values()):
                        current_room = None   # Ngăn finally gửi opponent_left
                        return

                    # ===== LÚC NÀY: CẢ 2 ĐÃ CHỌN =====
                    for p, v in list(current_room.rematch_votes.items()):
                        try:
                            if v is True:
                                # Người bấm YES → chỉ nhận thông báo
                                p.sendall(encode("opponent_left", {}))
                        except:
                            pass

                    # Dọn phòng hoàn toàn
                    if current_room in rooms:
                        rooms.remove(current_room)
                    if current_size and waiting.get(current_size) == current_room:
                        waiting[current_size] = None

                    current_room.players.clear()
                    current_room = None
                    return

                # ===== THOÁT KHI ĐANG CHƠI / ĐANG CHỜ =====
                # ===== THOÁT KHI ĐANG CHƠI / ĐANG CHỜ =====
                for p in current_room.players:
                    if p != conn:
                        try:
                            p.sendall(encode("opponent_left", {}))
                        except:
                            pass

                if current_room in rooms:
                    rooms.remove(current_room)
                if current_size and waiting.get(current_size) == current_room:
                    waiting[current_size] = None

                current_room.players.clear()
                current_room = None
                return

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")

    finally:
        print(f"[-] Client disconnected: {addr}")

        # Chỉ xử lý nếu vẫn còn đang ở trong room
        if current_room:
            for p in current_room.players:
                if p != conn:
                    try:
                        p.sendall(encode("opponent_left", {}))
                    except:
                        pass

            if current_room in rooms:
                rooms.remove(current_room)

            if current_size and waiting.get(current_size) == current_room:
                waiting[current_size] = None

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
