# client/ui_game.py
import tkinter as tk
from tkinter import messagebox

CELL_SIZE = 40

class GameScreen(tk.Frame):
    def __init__(self, master, app, size, symbol, your_turn):
        super().__init__(master)
        self.app = app
        self.size = size
        self.symbol = symbol
        self.your_turn = your_turn

        self.board = [[None]*size for _ in range(size)]

        self.status = tk.Label(self, text="", font=("Arial", 14))
        self.status.pack(pady=5)

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
        if self.your_turn:
            self.status.config(text=f"Bạn ({self.symbol}) - Lượt của bạn")
        else:
            self.status.config(text=f"Bạn ({self.symbol}) - Đang chờ đối thủ")

    def draw_grid(self):
        for i in range(self.size + 1):
            p = i * CELL_SIZE
            self.canvas.create_line(p, 0, p, self.size * CELL_SIZE)
            self.canvas.create_line(0, p, self.size * CELL_SIZE, p)

    def on_click(self, event):
        if not self.your_turn:
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
            messagebox.showinfo("Kết quả", "Bạn thắng!")
        else:
            messagebox.showinfo("Kết quả", "Bạn thua!")

        self.ask_rematch()

    def handle_draw(self):
        messagebox.showinfo("Kết quả", "Hòa!")
        self.ask_rematch()

    def ask_rematch(self):
        if messagebox.askyesno("Tiếp tục?", "Chơi lại ván mới?"):
            self.app.client.send("rematch", {})
        else:
            self.app.client.send("leave_room", {})
