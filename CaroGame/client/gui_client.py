import socket
import threading
import json
import tkinter as tk
from tkinter import messagebox

HOST = "127.0.0.1"
PORT = 5000

class CaroClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        self.window = tk.Tk()
        self.window.title("Caro Network Game")

        self.board_size = None
        self.symbol = None
        self.your_turn = False
        self.buttons = []

        self.create_menu()

        threading.Thread(target=self.listen_server, daemon=True).start()

        self.window.mainloop()

    # ================= MENU =================

    def create_menu(self):
        self.clear_window()

        tk.Label(self.window, text="Caro Network Game", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.window, text="Create room 3x3", width=20,
                  command=lambda: self.create_room(3)).pack(pady=5)

        tk.Button(self.window, text="Create room 10x10", width=20,
                  command=lambda: self.create_room(10)).pack(pady=5)

        tk.Button(self.window, text="Join room", width=20,
                  command=self.join_room).pack(pady=5)

    def create_room(self, size):
        msg = {"type": "create_room", "data": {"size": size}}
        self.sock.sendall(json.dumps(msg).encode())

    def join_room(self):
        msg = {"type": "join_room", "data": {}}
        self.sock.sendall(json.dumps(msg).encode())

    # ================= GAME BOARD =================

    def create_board(self, size):
        self.clear_window()
        self.buttons = []
        self.board_size = size

        info = tk.Label(self.window, text="", font=("Arial", 12))
        info.pack()
        self.info_label = info

        frame = tk.Frame(self.window)
        frame.pack()

        for i in range(size):
            row = []
            for j in range(size):
                btn = tk.Button(frame, text="", width=3, height=1,
                                font=("Arial", 14),
                                command=lambda x=i, y=j: self.on_click(x, y))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        self.update_turn_label()

    def update_turn_label(self):
        if self.your_turn:
            self.info_label.config(text="Your turn")
        else:
            self.info_label.config(text="Opponent's turn")

    def on_click(self, x, y):
        if not self.your_turn:
            return

        msg = {"type": "move", "data": {"x": x, "y": y}}
        self.sock.sendall(json.dumps(msg).encode())

    # ================= NETWORK =================

    def listen_server(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break

                msg = json.loads(data.decode())
                self.handle_message(msg)

            except Exception as e:
                print("Connection error:", e)
                break

    def handle_message(self, msg):
        msg_type = msg["type"]
        data = msg["data"]

        if msg_type == "room_created":
            print("Room created")

        elif msg_type == "start_game":
            self.symbol = data["symbol"]
            self.your_turn = data["your_turn"]
            size = data["size"]

            self.window.after(0, lambda: self.create_board(size))

        elif msg_type == "update":
            x = data["x"]
            y = data["y"]
            symbol = data["symbol"]

            self.window.after(0, lambda: self.update_cell(x, y, symbol))

        elif msg_type == "win":
            winner = data["winner"]
            self.window.after(0, lambda: self.show_result(winner))

        elif msg_type == "draw":
            self.window.after(0, lambda: messagebox.showinfo("Result", "Draw!"))

        elif msg_type == "error":
            message = data["message"]
            self.window.after(0, lambda: messagebox.showerror("Error", message))

    def update_cell(self, x, y, symbol):
        btn = self.buttons[x][y]
        btn.config(text=symbol, state="disabled")

        if symbol == self.symbol:
            self.your_turn = False
        else:
            self.your_turn = True

        self.update_turn_label()

    def show_result(self, winner):
        if winner == self.symbol:
            messagebox.showinfo("Result", "You win!")
        else:
            messagebox.showinfo("Result", "You lose!")

        self.create_menu()

    # ================= UTILS =================

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    CaroClient()
