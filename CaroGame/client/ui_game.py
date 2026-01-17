import tkinter as tk

CELL_SIZE = 40

class GameScreen(tk.Frame):
    def __init__(self, master, app, size, symbol, your_turn, score=None):
        super().__init__(master)
        self.app = app
        self.size = size
        self.symbol = symbol
        self.your_turn = your_turn
        self.menu_open = False
        self.opponent_left = False
        self.rematch_chosen = False

        self.board = [[None] * size for _ in range(size)]
        self.score = score if score else {"me": 0, "op": 0}

        # ===== THANH TRÊN =====
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x", pady=5)

        self.menu_btn = tk.Button(top_bar, text="☰", command=self.toggle_menu)
        self.menu_btn.pack(side="right", padx=10)

        # ===== TỈ SỐ =====
        self.score_label = tk.Label(
            self,
            font=("Arial", 13, "bold"),
            justify="center"
        )
        self.score_label.pack(pady=5)
        self.turn_label = tk.Label(
            self,
            font=("Arial", 12),
            fg="#34495e"
        )
        self.turn_label.pack(pady=(0, 6))


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
            self.turn_label.config(
                text="Đến lượt bạn",
                fg="#27ae60"   # xanh – đang được chơi
            )
        else:
            self.turn_label.config(
                text="Đang chờ đối thủ...",
                fg="#7f8c8d"   # xám – đang chờ
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
        if self.menu_open or not self.your_turn or hasattr(self, "overlay"):
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
            self.show_center_message("BẠN THẮNG", "#27ae60")
        else:
            self.score["op"] += 1
            self.show_center_message("BẠN THUA", "#e74c3c")

        self.app.score = self.score
        self.update_score()

        # Chỉ hỏi rematch nếu đối thủ chưa rời
        if not self.opponent_left:
            self.after(1500, self.ask_rematch)

    def handle_draw(self):
        self.show_center_message("HÒA", "#f39c12")

        if not self.opponent_left:
            self.after(1500, self.ask_rematch)

    def ask_rematch(self):
        if hasattr(self, "overlay"):
            try:
                self.overlay.destroy()
            except:
                pass
            del self.overlay

        self.rematch_chosen = False
        self.rematch_win = tk.Toplevel(self)
        self.rematch_win.title("Tiếp tục?")
        self.rematch_win.geometry("260x140")
        self.rematch_win.resizable(False, False)
        self.rematch_win.transient(self)
        self.rematch_win.grab_set()

        # ===== CĂN GIỮA THEO BÀN CỜ =====
        self.update_idletasks()
        self.rematch_win.update_idletasks()

        board_x = self.canvas.winfo_rootx()
        board_y = self.canvas.winfo_rooty()
        board_w = self.canvas.winfo_width()
        board_h = self.canvas.winfo_height()

        win_w = self.rematch_win.winfo_width()
        win_h = self.rematch_win.winfo_height()

        x = board_x + (board_w - win_w) // 2
        y = board_y + (board_h - win_h) // 2

        self.rematch_win.geometry(f"+{x}+{y}")

        # ===== NỘI DUNG =====
        tk.Label(
            self.rematch_win,
            text="Chơi lại ván mới?",
            font=("Arial", 12)
        ).pack(pady=20)

        btn_frame = tk.Frame(self.rematch_win)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="Có", width=8,
            command=self.on_yes_rematch
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame, text="Không", width=8,
            command=self.on_no_rematch
        ).pack(side="right", padx=10)

    def reset_board(self, size, symbol, your_turn):
        self.size = size
        self.symbol = symbol
        self.your_turn = your_turn
        self.opponent_left = False
        self.menu_open = False

        # Reset dữ liệu
        self.board = [[None] * size for _ in range(size)]

        # Xóa canvas và vẽ lại
        self.canvas.delete("all")
        self.canvas.config(
            width=size * CELL_SIZE,
            height=size * CELL_SIZE
        )
        self.draw_grid()

        self.update_status()
        if hasattr(self, "overlay"):
            try:
                self.overlay.destroy()
            except:
                pass
            del self.overlay

    def handle_opponent_left(self):
        self.opponent_left = True
        self.your_turn = False

        # Nếu đang có cửa sổ rematch thì đóng nó
        if hasattr(self, "rematch_win"):
            try:
                self.rematch_win.destroy()
            except:
                pass
            del self.rematch_win

        # Trường hợp người này đã bấm YES rồi
        if self.rematch_chosen:
            # Hiển thị thông báo rõ ràng
            self.show_center_message(
                "Đối thủ không muốn chơi tiếp\nĐang quay về menu...",
                "#c0392b"
            )

            # Chờ một chút cho người chơi đọc xong rồi mới out
            self.after(1500, lambda: self.app.client.send("leave_room", {}))
            return

        # Trường hợp chưa bấm Yes/No (đang chơi hoặc vừa kết thúc ván)
        self.show_center_message("ĐỐI THỦ ĐÃ THOÁT", "#c0392b")

        # Nếu đang ở giai đoạn hỏi rematch
        if hasattr(self, "rematch_win"):
            try:
                self.rematch_win.destroy()
            except:
                pass
            del self.rematch_win

        # Cho người chơi nhìn thấy thông báo một chút rồi mới out
        self.after(1500, lambda: self.app.client.send("leave_room", {}))

    def on_yes_rematch(self):
        self.rematch_chosen = True

        if self.opponent_left:
            self.show_center_message(
                "Không còn đối thủ\nĐang quay về menu...",
                "#c0392b"
            )
            if hasattr(self, "rematch_win"):
                self.rematch_win.destroy()
            self.after(1500, lambda: self.app.client.send("leave_room", {}))
            return

        if hasattr(self, "rematch_win"):
            self.rematch_win.destroy()

        self.app.client.send("rematch", {})


    def on_no_rematch(self):
        self.rematch_chosen = True
        if hasattr(self, "rematch_win"):
            self.rematch_win.destroy()
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

        if self.opponent_left:
            self.show_center_message(
                "Không còn đối thủ\nHãy thoát để tìm trận mới",
                "#c0392b"
            )
            return

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

    def show_center_message(self, text, color="#2c3e50", subtitle=None):
        # Xóa overlay cũ nếu có
        if hasattr(self, "overlay"):
            try:
                self.overlay.destroy()
            except:
                pass
            del self.overlay

        self.overlay = tk.Frame(
            self,
            bg="#fdfefe",
            bd=4,
            relief="ridge"
        )

        title = tk.Label(
            self.overlay,
            text=text,
            font=("Arial", 22, "bold"),
            fg=color,
            bg="#fdfefe",
            justify="center"
        )
        title.pack(padx=35, pady=(22, 8))

        if subtitle:
            sub = tk.Label(
                self.overlay,
                text=subtitle,
                font=("Arial", 12),
                fg="#555",
                bg="#fdfefe",
                justify="center"
            )
            sub.pack(padx=25, pady=(0, 18))

        # Đặt overlay ở giữa bàn cờ
        self.update_idletasks()
        x = self.canvas.winfo_x() + self.canvas.winfo_width() // 2
        y = self.canvas.winfo_y() + self.canvas.winfo_height() // 2
        self.overlay.place(anchor="center", x=x, y=y)
