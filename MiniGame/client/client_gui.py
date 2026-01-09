import socket
import json
import tkinter as tk
from tkinter import messagebox

from config import HOST, PORT, BUFFER_SIZE


class RPSClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keo - Bua - Bao")
        self.root.geometry("420x420")
        self.root.resizable(False, False)

        # Ket noi server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Loi", str(e))
            root.destroy()
            return

        # ====== TIEU DE ======
        tk.Label(
            root,
            text="TRO CHOI KEO - BUA - BAO",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ====== TI SO ======
        tk.Label(
            root,
            text="TỈ SỐ",
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        # ====== KHUNG TI SO ======
        score_frame = tk.Frame(root)
        score_frame.pack(pady=10, fill="x")

        # ---- CLIENT ----
        client_frame = tk.Frame(score_frame)
        client_frame.pack(side="left", expand=True)

        tk.Label(
            client_frame,
            text="CLIENT",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        self.client_score_box = tk.Label(
            client_frame,
            text="0",
            font=("Arial", 18, "bold"),
            width=6,
            height=2,
            relief="solid",
            bd=2,
            fg="green"
        )
        self.client_score_box.pack()

        # ---- SERVER ----
        server_frame = tk.Frame(score_frame)
        server_frame.pack(side="right", expand=True)

        tk.Label(
            server_frame,
            text="SERVER",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        self.server_score_box = tk.Label(
            server_frame,
            text="0",
            font=("Arial", 18, "bold"),
            width=6,
            height=2,
            relief="solid",
            bd=2,
            fg="red"
        )
        self.server_score_box.pack()

        # ====== NUT CHON ======
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        for i, c in enumerate(["keo", "bua", "bao"]):
            tk.Button(
                btn_frame,
                text=c.upper(),
                width=10,
                command=lambda x=c: self.play(x)
            ).grid(row=0, column=i, padx=5)

        # ====== KET QUA ======
        self.result_label = tk.Label(
            root,
            text="Hay chon nuoc di",
            font=("Arial", 12)
        )
        self.result_label.pack(pady=10)

        self.server_choice_label = tk.Label(root, text="")
        self.server_choice_label.pack()

        # ====== THOAT ======
        tk.Button(
            root,
            text="THOAT",
            width=15,
            command=self.exit_game
        ).pack(pady=20)

    def play(self, choice):
        try:
            self.client_socket.send(choice.encode())
            result = json.loads(
                self.client_socket.recv(BUFFER_SIZE).decode()
            )

            if result["status"] == "ok":
                c = result["client_score"]
                s = result["server_score"]

                self.client_score_box.config(text=str(c))
                self.server_score_box.config(text=str(s))

                self.result_label.config(
                    text=f"Ket qua: BAN {result['ket_qua'].upper()}"
                )
                self.server_choice_label.config(
                    text=f"Server chon: {result['lua_chon_server'].upper()}"
                )
            else:
                messagebox.showwarning("Loi", result["message"])

        except Exception as e:
            messagebox.showerror("Loi", str(e))
            self.root.destroy()

    def exit_game(self):
        try:
            self.client_socket.send("thoat".encode())
        except:
            pass
        self.client_socket.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    RPSClientGUI(root)
    root.mainloop()
