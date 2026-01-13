import tkinter as tk

class MenuScreen(tk.Frame):
    def __init__(self, master, client):
        super().__init__(master)
        self.client = client

        tk.Label(
            self,
            text="CARO GAME",
            font=("Arial", 28, "bold")
        ).pack(pady=40)

        self.size_var = tk.IntVar(value=3)

        size_frame = tk.Frame(self)
        size_frame.pack(pady=20)

        tk.Radiobutton(
            size_frame, text="Bàn cờ 3 x 3",
            variable=self.size_var, value=3,
            font=("Arial", 14)
        ).pack(anchor="w", pady=5)

        tk.Radiobutton(
            size_frame, text="Bàn cờ 10 x 10",
            variable=self.size_var, value=10,
            font=("Arial", 14)
        ).pack(anchor="w", pady=5)

        # ===== NÚT BẮT ĐẦU =====
        self.btn_start = tk.Button(
            self, text="Bắt đầu chơi",
            font=("Arial", 16),
            width=20, height=2,
            command=self.quick_play
        )
        self.btn_start.pack(pady=20)

        # ===== NÚT HỦY =====
        self.btn_cancel = tk.Button(
            self, text="Hủy",
            font=("Arial", 14),
            width=10,
            command=self.cancel_search
        )
        # Ẩn lúc đầu
        self.btn_cancel.pack(pady=5)
        self.btn_cancel.pack_forget()

        self.status = tk.Label(self, text="", font=("Arial", 12))
        self.status.pack(pady=10)

    def quick_play(self):
        size = self.size_var.get()

        self.btn_start.config(state="disabled")
        self.btn_cancel.pack()  # 🔥 hiện nút Hủy

        self.status.config(text="Đang tìm đối thủ...")
        self.client.send("quick_play", {"size": size})

    def cancel_search(self):
        # Gửi thông báo rời phòng chờ
        self.client.send("leave_room", {})

        self.status.config(text="Đã hủy tìm đối thủ.")
        self.btn_start.config(state="normal")
        self.btn_cancel.pack_forget()  # 🔥 ẩn nút Hủy

    def set_status(self, text):
        self.status.config(text=text)

        # Khi quay menu / bị out
        if "menu" in text.lower() or "thoát" in text.lower():
            self.btn_start.config(state="normal")
            self.btn_cancel.pack_forget()
