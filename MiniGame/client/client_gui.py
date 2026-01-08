import socket
import json
import tkinter as tk
from tkinter import messagebox

from config import HOST, PORT, BUFFER_SIZE


class RPSClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tro choi Keo - Bua - Bao")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Ket noi server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Loi", f"Khong ket noi duoc server:\n{e}")
            root.destroy()
            return

        # Tieu de
        title = tk.Label(
            root,
            text="TRO CHOI KEO - BUA - BAO",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # Nut lua chon
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="KEO", width=10,
                  command=lambda: self.play("keo")).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="BUA", width=10,
                  command=lambda: self.play("bua")).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="BAO", width=10,
                  command=lambda: self.play("bao")).grid(row=0, column=2, padx=5)

        # Ket qua
        self.result_label = tk.Label(root, text="Hay chon nuoc di",
                                     font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.server_choice_label = tk.Label(root, text="")
        self.server_choice_label.pack()

        # Nut thoat
        tk.Button(root, text="THOAT", width=15,
                  command=self.exit_game).pack(pady=20)

    def play(self, choice):
        try:
            self.client_socket.send(choice.encode())
            response = self.client_socket.recv(BUFFER_SIZE).decode()
            result = json.loads(response)

            if result["status"] == "ok":
                self.result_label.config(
                    text=f"Ket qua: BAN {result['ket_qua'].upper()}"
                )
                self.server_choice_label.config(
                    text=f"Server chon: {result['lua_chon_server'].upper()}"
                )
            else:
                messagebox.showwarning("Loi", result["message"])

        except Exception as e:
            messagebox.showerror("Loi", f"Mat ket noi server:\n{e}")
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
    app = RPSClientGUI(root)
    root.mainloop()
