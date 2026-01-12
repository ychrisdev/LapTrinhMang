# client/ui_game.py
import tkinter as tk
from tkinter import messagebox

CELL_SIZE = 40

class GameScreen(tk.Frame):
    def __init__(self, master, app, size, symbol, your_turn, score=None):
        super().__init__(master)
        self.app = app
        self.size = size
        self.symbol = symbol
        self.your_turn = your_turn

        self.paused = False
        self.opponent_paused = False

        self.board = [[None] * size for _ in range(size)]
        self.score = score if score else {"me": 0, "op": 0}

        # Thanh trên
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x", pady=5)

        self.status = tk.Label(top_bar, text="", font=("Arial", 14))
        self.status.pack(side="left", padx=10)

        self.menu_btn = tk.Button(top_bar, text="☰", command=self.toggle_menu)
        self.menu_btn.pack(side="right", padx=10)

        # Hiển thị tỉ số
        self.score_label = tk.Label(
            self,
            text="Tỉ số\nBạn 0 - 0 Đối thủ",
            font=("Arial", 13, "bold"),
            justify="center",
            anchor="center"
        )
        self.score_label.pack(pady=5)

        # Menu nổi
        self.menu_frame = tk.Frame(self, bd=2, relief="ridge")
        self.menu_frame.pack(pady=5)
        self.menu_frame.pack_forget()

        tk.Button(self.menu_frame, text="Tiếp tục", width=15, command=self.resume).pack(pady=2)
        tk.Button(self.menu_frame, text="Tạm dừng", width=15, command=self.pause).pack(pady=2)
        tk.Button(self.menu_frame, text="Thoát", width=15, command=self.leave).pack(pady=2)

        # Bàn cờ
        self.canvas = tk.Canvas(
            self,
            width=size * CELL_SIZE,
            height=size * CELL_SIZE,
            bg="white"
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.update_status()
        self.draw_grid()

    def update_status(self):
        if self.paused:
            self.status.config(
                text="Bạn đang tạm dừng ván đấu",
                fg="gray"
            )
        elif self.opponent_paused:
            self.status.config(
                text="Đối thủ đang tạm dừng ván đấu",
                fg="red"
            )
        elif self.your_turn:
            self.status.config(
                text=f"Bạn ({self.symbol}) - Lượt của bạn",
                fg="green"
            )
        else:
            self.status.config(
                text=f"Bạn ({self.symbol}) - Đang chờ đối thủ",
                fg="blue"
            )

    def update_score(self):
        self.score_label.config(
            text=f"Tỉ số\nBạn {self.score['me']} - {self.score['op']} Đối thủ",
            font=("Arial", 13, "bold"),
            justify="center",
            anchor="center"
        )

    def draw_grid(self):
        for i in range(self.size + 1):
            p = i * CELL_SIZE
            self.canvas.create_line(p, 0, p, self.size * CELL_SIZE)
            self.canvas.create_line(0, p, self.size * CELL_SIZE, p)

    def on_click(self, event):
        if self.paused or self.opponent_paused or not self.your_turn:
            return

        x = event.y // CELL_SIZE
        y = event.x // CELL_SIZE

        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return

        if self.board[x][y] is not None:
            return

        self.app.client.send("move", {"x": x, "y": y})
        self.your_turn = False
        self.update_status()

    def handle_update(self, x, y, symbol):
        self.board[x][y] = symbol

        cx = y * CELL_SIZE + CELL_SIZE // 2
        cy = x * CELL_SIZE + CELL_SIZE // 2

        self.canvas.create_text(cx, cy, text=symbol, font=("Arial", 18))

        if symbol != self.symbol:
            self.your_turn = True
            self.update_status()

    def handle_win(self, winner):
        if winner == self.symbol:
            self.score["me"] += 1
            messagebox.showinfo("Kết quả", "Bạn thắng!")
        else:
            self.score["op"] += 1
            messagebox.showinfo("Kết quả", "Bạn thua!")

        self.update_score()
        self.ask_rematch()

    def handle_draw(self):
        messagebox.showinfo("Kết quả", "Hòa!")
        self.ask_rematch()

    def ask_rematch(self):
        if messagebox.askyesno("Tiếp tục?", "Chơi lại ván mới?"):
            self.app.client.send("rematch", {})
        else:
            self.app.client.send("leave_room", {})

    def toggle_menu(self):
        if self.menu_frame.winfo_ismapped():
            self.menu_frame.pack_forget()
        else:
            self.menu_frame.pack(pady=5)

    def pause(self):
        if self.paused:
            return
        self.paused = True
        self.menu_frame.pack_forget()
        self.update_status()
        self.app.client.send("pause", {})

    def resume(self):
        if not self.paused:
            return
        self.paused = False
        self.menu_frame.pack_forget()
        self.update_status()
        self.app.client.send("resume", {})

    def leave(self):
        self.app.client.send("leave_room", {})

    def handle_opponent_pause(self):
        self.opponent_paused = True
        self.update_status()

    def handle_opponent_resume(self):
        self.opponent_paused = False
        self.update_status()
