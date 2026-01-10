import socket
import json
import tkinter as tk
from tkinter import messagebox

from config import HOST, PORT, BUFFER_SIZE


ICON_MAP = {
    "keo": "✌️",
    "bua": "✊",
    "bao": "✋"
}


class RPSClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keo - Bua - Bao")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        self.history = []

        # ===== KET NOI SERVER =====
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Loi", str(e))
            root.destroy()
            return

        # ===== NUT DUNG LAI =====
        btn_bottom = tk.Frame(root)
        btn_bottom.pack(pady=10)

        tk.Button(
            btn_bottom,
            text="DUNG LAI",
            width=12,
            command=self.pause_menu
        ).pack()

        # ===== TIEU DE =====
        tk.Label(
            root,
            text="TRO CHOI KEO - BUA - BAO",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # ===== TI SO =====
        tk.Label(
            root,
            text="TỈ SỐ",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        score_frame = tk.Frame(root)
        score_frame.pack(pady=10, fill="x")

        # CLIENT
        client_frame = tk.Frame(score_frame)
        client_frame.pack(side="left", expand=True)

        tk.Label(client_frame, text="CLIENT",
                 font=("Arial", 10, "bold")).pack()

        self.client_score_box = tk.Label(
            client_frame, text="0",
            font=("Arial", 14, "bold"),
            width=6, height=2,
            relief="solid", bd=2,
            fg="green"
        )
        self.client_score_box.pack()

        # SERVER
        server_frame = tk.Frame(score_frame)
        server_frame.pack(side="right", expand=True)

        tk.Label(server_frame, text="SERVER",
                 font=("Arial", 10, "bold")).pack()

        self.server_score_box = tk.Label(
            server_frame, text="0",
            font=("Arial", 14, "bold"),
            width=6, height=2,
            relief="solid", bd=2,
            fg="red"
        )
        self.server_score_box.pack()

        # ===== ICON HIEN THI CHINH GIUA =====
        icon_frame = tk.Frame(root)
        icon_frame.pack(pady=30)

        self.client_icon = tk.Label(
            icon_frame, text="❔",
            font=("Arial", 50),
            fg="green"
        )
        self.client_icon.pack(side="left", padx=60)

        self.server_icon = tk.Label(
            icon_frame, text="❔",
            font=("Arial", 50),
            fg="red"
        )
        self.server_icon.pack(side="right", padx=60)

        # ===== KET QUA =====
        self.result_label = tk.Label(
            root,
            text="Hay chon nuoc di",
            font=("Arial", 12)
        )
        self.result_label.pack()

        # ===== NUT CHON ICON =====
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=25)

        for i, c in enumerate(["keo", "bua", "bao"]):
            tk.Button(
                btn_frame,
                text=ICON_MAP[c],
                font=("Arial", 22),
                width=3,
                command=lambda x=c: self.play(x)
            ).grid(row=0, column=i, padx=15)

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

                # ICON HIEN THI
                self.client_icon.config(
                    text=ICON_MAP[result["lua_chon_client"]],
                    fg="green"
                )
                self.server_icon.config(
                    text=ICON_MAP[result["lua_chon_server"]],
                    fg="red"
                )

                self.result_label.config(
                    text=f"Ket qua: BAN {result['ket_qua'].upper()}"
                )

                # LUU LICH SU
                self.history.append({
                    "client": result["lua_chon_client"],
                    "server": result["lua_chon_server"],
                    "ket_qua": result["ket_qua"]
                })

            else:
                messagebox.showwarning("Loi", result["message"])

        except Exception as e:
            messagebox.showerror("Loi", str(e))
            self.root.destroy()

    # ===== PAUSE MENU =====
    def pause_menu(self):
        pause_window = tk.Toplevel(self.root)
        self.pause_window = pause_window

        pause_window.title("Tam dung")
        pause_window.geometry("300x200")
        pause_window.resizable(False, False)
        pause_window.transient(self.root)
        pause_window.grab_set()

        tk.Label(
            pause_window,
            text="TAM DUNG GAME",
            font=("Arial", 12, "bold")
        ).pack(pady=15)

        tk.Button(
            pause_window,
            text="LICH SU",
            width=15,
            command=self.show_history
        ).pack(pady=5)

        tk.Button(
            pause_window,
            text="TIEP TUC",
            width=15,
            command=pause_window.destroy
        ).pack(pady=5)

        tk.Button(
            pause_window,
            text="THOAT",
            width=15,
            command=self.exit_game
        ).pack(pady=5)

    def show_history(self):
        if not self.history:
            messagebox.showinfo(
                "Lich su",
                "Chua co nuoc di nao.",
                parent=self.pause_window
            )
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Lich su")
        history_window.geometry("360x320")
        history_window.resizable(False, False)

        self.pause_window.grab_release()
        history_window.grab_set()

        text = tk.Text(history_window, height=12)
        text.pack(padx=5, pady=5, fill="both")

        for i, h in enumerate(self.history, start=1):
            text.insert(
                "end",
                f"Van {i}: {h['client']} - {h['server']} → {h['ket_qua']}\n"
            )

        text.config(state="disabled")

        tk.Button(
            history_window,
            text="QUAY LAI",
            width=12,
            command=history_window.destroy
        ).pack(pady=8)

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
