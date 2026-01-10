import socket
import json
import tkinter as tk
from tkinter import messagebox

from config import HOST, PORT, BUFFER_SIZE


class RPSClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keo - Bua - Bao")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        self.history = []

        # Ket noi server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Loi", str(e))
            root.destroy()
            return

        btn_bottom = tk.Frame(root)
        btn_bottom.pack(pady=15)
        
        tk.Button(
            btn_bottom,
            text="DUNG LAI",
            width=12,
            command=self.pause_menu
        ).grid(row=0, column=1, padx=5)


        # ====== TIEU DE ======
        tk.Label(
            root,
            text="TRO CHOI KEO - BUA - BAO",
            font=("Arial", 20, "bold")
        ).pack(pady=40)

        # ====== TI SO ======
        tk.Label(
            root,
            text="TỈ SỐ",
            font=("Arial", 12, "bold")
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
            font=("Arial", 10, "bold")
        ).pack(pady=5)

        self.client_score_box = tk.Label(
            client_frame,
            text="0",
            font=("Arial", 11, "bold"),
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
            font=("Arial", 10, "bold")
        ).pack(pady=5)

        self.server_score_box = tk.Label(
            server_frame,
            text="0",
            font=("Arial", 11, "bold"),
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

                # Luu lich su
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

    def exit_game(self):
        try:
            self.client_socket.send("thoat".encode())
        except:
            pass
        self.client_socket.close()
        self.root.destroy()

    def show_history(self):
        # ===== CHUA CO LICH SU =====
        if not self.history:
            messagebox.showinfo(
                "Lich su",
                "Chua co nuoc di nao.\nHay choi it nhat 1 van.",
                parent=self.pause_window
            )
            return

        # ===== CO LICH SU =====
        history_window = tk.Toplevel(self.root)
        history_window.title("Lich su nuoc di")
        history_window.geometry("350x320")
        history_window.resizable(False, False)

        # 🔑 Chuyen quyen tu PAUSE sang HISTORY
        self.pause_window.grab_release()
        history_window.transient(self.pause_window)
        history_window.grab_set()

        text = tk.Text(history_window, wrap="word", height=12)
        text.pack(expand=True, fill="both", padx=5, pady=5)

        for i, h in enumerate(self.history, start=1):
            text.insert(
                "end",
                f"Van {i}: Ban chon {h['client']} | "
                f"Server chon {h['server']} | "
                f"Ket qua: {h['ket_qua']}\n"
            )

        text.config(state="disabled")

        # ===== NUT QUAY LAI =====
        def back_to_pause():
            history_window.grab_release()
            self.pause_window.grab_set()
            history_window.destroy()

        tk.Button(
            history_window,
            text="QUAY LAI",
            width=12,
            command=back_to_pause
        ).pack(pady=8)

        # Khi bam X tren cua so
        history_window.protocol("WM_DELETE_WINDOW", back_to_pause)



    def pause_menu(self):
        pause_window = tk.Toplevel(self.root)
        self.pause_window = pause_window 
        
        pause_window.title("Tam dung")
        pause_window.geometry("300x200")
        pause_window.resizable(False, False)

        pause_window.transient(self.root)
        pause_window.grab_set() #chặn chơi

        tk.Label(
            pause_window,
            text="TAM DUNG GAME",
            font=("Arial", 12, "bold")
        ).pack(pady=15)

        btn_frame = tk.Frame(pause_window)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="LICH SU",
            width=15,
            command= self.show_history
        ).pack(pady=5)

        tk.Button(
            btn_frame,
            text="TIEP TUC",
            width=15,
            command=pause_window.destroy
        ).pack(pady=5)

        tk.Button(
            btn_frame,
            text="THOAT",
            width=15,
            command=self.exit_game
        ).pack(pady=5)



if __name__ == "__main__":
    root = tk.Tk()
    RPSClientGUI(root)
    root.mainloop()
