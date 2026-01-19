import tkinter as tk



class GameScreen(tk.Frame):
    def __init__(self, master, app, size, symbol, your_turn, score=None):
        super().__init__(master)
        self.app = app
        self.size = size
        self.symbol = symbol
        self.your_turn = your_turn
        self.setup_ui_config()
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

        # ===== KHUNG TỈ SỐ =====
        self.score_frame = tk.Frame(
            self,
            bd=2,
            relief="groove",
            bg="#fdfefe",
            padx=self.score_padx,
            pady=self.score_pady
        )
        self.score_frame.pack(pady=(6, 10))

        # Tiêu đề
        tk.Label(
            self.score_frame,
            text="TỈ SỐ",
            font=("Arial", self.score_title_font, "bold"),
            fg="#2c3e50",
            bg="#fdfefe"
        ).pack(pady=(0, 4))

        # Hàng hiển thị điểm
        row = tk.Frame(self.score_frame, bg="#fdfefe")
        row.pack()

        # ===== BẠN =====
        tk.Label(
            row,
            text="Bạn",
            font=("Arial", self.score_title_font),
            bg="#fdfefe"
        ).grid(row=0, column=0)

        self.me_score_label = tk.Label(
            row,
            text="0",
            font=("Arial", self.score_font, "bold"),
            fg="#27ae60",
            bg="#fdfefe",
            width=3
        )
        self.me_score_label.grid(row=1, column=0)

        # ===== PHÂN CÁCH =====
        tk.Label(
            row,
            text="—",
            font=("Arial", self.score_font),
            bg="#fdfefe"
        ).grid(row=1, column=1, padx=12)

        # ===== ĐỐI THỦ =====
        tk.Label(
            row,
            text="Đối thủ",
            font=("Arial", self.score_title_font),
            bg="#fdfefe"
        ).grid(row=0, column=2)

        self.op_score_label = tk.Label(
            row,
            text="0",
            font=("Arial", self.score_font, "bold"),
            fg="#e74c3c",
            bg="#fdfefe",
            width=3
        )
        self.op_score_label.grid(row=1, column=2)

        
        self.turn_label = tk.Label(
            self,
            font=("Arial", self.turn_font),
            fg="#34495e"
        )
        self.turn_label.pack(pady=self.turn_pady)


        self.update_score()
        # ===== MENU NỔI =====
        self.menu_frame = tk.Frame(self, bd=2, relief="ridge", bg="white", pady=8)
        self.menu_frame.place_forget()

        tk.Button(
            self.menu_frame, text="Tiếp tục",
            width=self.menu_btn_width, command=self.resume
        ).pack(pady=4)

        tk.Button(
            self.menu_frame, text="Luật chơi",
            width=self.menu_btn_width, command=self.show_rules
        ).pack(pady=4)

        tk.Button(
            self.menu_frame, text="Thoát",
            width=self.menu_btn_width, command=self.leave
        ).pack(pady=4)

        self.canvas = tk.Canvas(
            self,
            width=self.size * self.cell_size,
            height=self.size * self.cell_size,
            bg="#E8D5B7",
            highlightthickness=0
        )
        self.canvas.pack(pady=self.canvas_pady)

        self.canvas.bind("<Button-1>", self.on_click)

        self.update_status()
        self.draw_grid()

    # ================= SCORE =================
    def update_score(self):
        self.me_score_label.config(text=str(self.score["me"]))
        self.op_score_label.config(text=str(self.score["op"]))

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


    
    # ================= GRID =================
    def draw_grid(self):
        for i in range(self.size + 1):
            p = i * self.cell_size
            self.canvas.create_line(
                p, 0, p, self.size * self.cell_size,
                fill="#8B5A2B", width=2
            )
            self.canvas.create_line(
                0, p, self.size * self.cell_size, p,
                fill="#8B5A2B", width=2
            )

    # ================= CLICK =================
    def on_click(self, event):
        if self.menu_open or not self.your_turn or hasattr(self, "overlay"):
            return

        x = event.y // self.cell_size
        y = event.x // self.cell_size

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

        cx = y * self.cell_size + self.cell_size // 2
        cy = x * self.cell_size + self.cell_size // 2
        color = "#c0392b" if symbol == "X" else "#2980b9"

        self.canvas.create_text(
            cx,
            cy,
            text=symbol,
            font=("Arial", self.xo_font_size, "bold"),
            fill=color
        )


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
            width=size * self.cell_size,
            height=size * self.cell_size
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

           # ===== KÍCH THƯỚC MENU =====
            menu_w = 140
            menu_h = 130

            x = bx - fx + self.menu_btn.winfo_width() - menu_w
            y = by - fy

            self.menu_frame.place(
                x=x,
                y=y,
                width=menu_w,
                height=menu_h
            )

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

        # ===== CĂN GIỮA THEO BÀN CỜ =====
        self.update_idletasks()
        rule_window.update_idletasks()

        board_x = self.canvas.winfo_rootx()
        board_y = self.canvas.winfo_rooty()
        board_w = self.canvas.winfo_width()
        board_h = self.canvas.winfo_height()

        win_w = rule_window.winfo_width()
        win_h = rule_window.winfo_height()

        x = board_x + (board_w - win_w) // 2
        y = board_y + (board_h - win_h) // 2 - 120

        rule_window.geometry(f"+{x}+{y}")

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

    def setup_ui_config(self):
        if self.size == 3:
            # ===== 3x3 =====
            self.cell_size = 120  #kích thước ô
            self.xo_font_size = 64   #kich thước X,O

            self.score_font = 22
            self.score_title_font = 18
            self.score_padx = 18        #độ rộng khug tỉ số
            self.score_pady = 8         #độ dài khug tỉ số

            self.turn_font = 14         #Cỡ chữ dòng “Đến lượt bạn / đối thủ”
            self.turn_pady = (6, 0)     # Khoảng cách trên/dưới dòng lượt chơi

            self.canvas_pady = (30, 0)   # khoảng cách trên/dưới bàn cờ
            self.menu_btn_width = 15

        else:
            # ===== 10x10 =====
            self.cell_size = 50
            self.xo_font_size = 28

            self.score_font = 16
            self.score_title_font = 12
            self.score_padx = 10
            self.score_pady = 5

            self.turn_font = 12
            self.turn_pady = (0, 4)

            self.canvas_pady = (6, 0)
            self.menu_btn_width = 15
    