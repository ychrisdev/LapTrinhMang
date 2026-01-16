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
        self.menu_open = False

        self.board = [[None] * size for _ in range(size)]
        self.score = score if score else {"me": 0, "op": 0}

        # ===== THANH TRÊN =====
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x", pady=5)

        self.status = tk.Label(top_bar, text="", font=("Arial", 14))
        self.status.pack(side="left", padx=10)

        self.menu_btn = tk.Button(top_bar, text="☰", command=self.toggle_menu)
        self.menu_btn.pack(side="right", padx=10)

        # ===== TỈ SỐ =====
        self.score_label = tk.Label(
            self,
            font=("Arial", 13, "bold"),
            justify="center"
        )
        self.score_label.pack(pady=5)

        self.update_score()
        # ===== MENU NỔI =====
        self.menu_frame = tk.Frame(self, bd=2, relief="ridge", bg="white")
        self.menu_frame.place_forget()



        tk.Button(
            self.menu_frame, text="Tiếp tục",
            width=15, command=self.resume
        ).pack(pady=4)

        tk.Button(
            self .menu_frame, text="luật chơi",
            width=15, command=self .show_rules
        ) .pack(pady=4)

        tk.Button(
            self.menu_frame, text="Thoát",
            width=15, command=self.leave
        ).pack(pady=4)

        # ===== BÀN CỜ =====
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

    # ================= STATUS =================
    def update_status(self):
        if self.your_turn:
            self.status.config(
                text=f"Bạn ({self.symbol}) - Lượt của bạn",
                fg="green"
            )
        else:
            self.status.config(
                text=f"Bạn ({self.symbol}) - Đang chờ đối thủ",
                fg="blue"
            )

    # ================= SCORE =================
    def update_score(self):
        self.score_label.config(
            text=f"Tỉ số\nBạn {self.score['me']} - {self.score['op']} Đối thủ"
        )

    # ================= GRID =================
    def draw_grid(self):
        for i in range(self.size + 1):
            p = i * CELL_SIZE
            self.canvas.create_line(p, 0, p, self.size * CELL_SIZE)
            self.canvas.create_line(0, p, self.size * CELL_SIZE, p)

    # ================= CLICK =================
    def on_click(self, event):
        if self.menu_open or not self.your_turn:
            return

        x = event.y // CELL_SIZE
        y = event.x // CELL_SIZE

        if not (0 <= x < self.size and 0 <= y < self.size):
            return

        if self.board[x][y] is not None:
            return

        self.app.client.send("move", {"x": x, "y": y})
        self.your_turn = False
        self.update_status()

    # ================= UPDATE =================
    def handle_update(self, x, y, symbol):
        self.board[x][y] = symbol

        cx = y * CELL_SIZE + CELL_SIZE // 2
        cy = x * CELL_SIZE + CELL_SIZE // 2
        self.canvas.create_text(cx, cy, text=symbol, font=("Arial", 18))

        if symbol != self.symbol:
            self.your_turn = True
            self.update_status()

    # ================= KẾT THÚC =================
    def handle_win(self, winner):
        if winner == self.symbol:
            self.score["me"] += 1
            self.status.config(text="Bạn đã thắng ván này!", fg="green")
        else:
            self.score["op"] += 1
            self.status.config(text="Bạn đã thua ván này!", fg="red")

        # 🔥 ĐỒNG BỘ VỀ APP
        self.app.score = self.score

        self.update_score()
        self.after(300, self.ask_rematch)


    def handle_draw(self):
        self.status.config(text="Ván đấu hòa!", fg="orange")
        self.after(300, self.ask_rematch)

    def ask_rematch(self):
        if messagebox.askyesno("Tiếp tục?", "Chơi lại ván mới?"):
            self.app.client.send("rematch", {})
        else:
            self.app.client.send("leave_room", {})

    # ================= MENU =================
    def toggle_menu(self):
        if self.menu_open:
            self.menu_frame.place_forget()
            self.menu_open = False
        else:
            self.menu_btn.update_idletasks()
            self.menu_frame.update_idletasks()

            bx = self.menu_btn.winfo_rootx()
            by = self.menu_btn.winfo_rooty() + self.menu_btn.winfo_height()

            fx = self.winfo_rootx()
            fy = self.winfo_rooty()

            x = bx - fx + self.menu_btn.winfo_width() - self.menu_frame.winfo_reqwidth()
            y = by - fy

            self.menu_frame.place(x=x, y=y)
            self.menu_frame.lift()   # ÉP MENU NỔI LÊN TRÊN CANVAS
            self.menu_open = True



    def resume(self):
        self.menu_frame.place_forget()
        self.menu_open = False
        self.update_status()


    def leave(self):
        self.app.is_leaving = True
        self.app.client.send("leave_room", {})

    def show_rules(self):
        rule_win = "3 ô liên tiếp" if self.size == 3 else "5 ô liên tiếp"
        board_size = "3 x 3" if self.size == 3 else "10 x 10"

        # ===== CỬA SỔ LUẬT CHƠI =====
        rule_window = tk.Toplevel(self)
        rule_window.title("Luật chơi")
        rule_window.geometry("320x280")
        rule_window.resizable(False, False)
        rule_window.transient(self)
        rule_window.grab_set()

        # ===== KHUNG CHÍNH =====
        container = tk.Frame(rule_window, padx=20, pady=15)
        container.pack(fill="both", expand=True)

        # ===== TIÊU ĐỀ =====
        tk.Label(
            container,
            text="LUẬT CHƠI CARO",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=(0, 10))

        # ===== NỘI DUNG =====
        tk.Label(
            container,
            text=f"Bàn cờ: {board_size}",
            font=("Arial", 13)
        ).pack(pady=5)

        tk.Label(
            container,
            text=f"Điều kiện thắng:",
            font=("Arial", 13, "bold")
        ).pack(pady=(10, 2))

        tk.Label(
            container,
            text=rule_win,
            font=("Arial", 14),
            fg="#e74c3c"
        ).pack(pady=5)

        # ===== NÚT ĐÓNG =====
        tk.Button(
            container,
            text="Đóng",
            font=("Arial", 12),
            width=14,
            height=1,
            command=rule_window.destroy
        ).pack(pady=15)

        # Đóng menu nổi sau khi mở luật
        self.menu_frame.place_forget()
        self.menu_open = False
