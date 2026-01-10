# client/ui_menu.py
import tkinter as tk

class MenuScreen(tk.Frame):
    def __init__(self, master, client):
        super().__init__(master)
        self.client = client

        tk.Label(
            self,
            text="CARO ONLINE",
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

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=40)

        tk.Button(
            btn_frame, text="Tạo phòng",
            font=("Arial", 16),
            width=15, height=2,
            command=self.create_room
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            btn_frame, text="Tham gia phòng",
            font=("Arial", 16),
            width=15, height=2,
            command=self.join_room
        ).grid(row=0, column=1, padx=20)

    def create_room(self):
        size = self.size_var.get()
        self.client.send("create_room", {"size": size})

    def join_room(self):
        self.client.send("join_room", {})
