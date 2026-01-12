import socket
import json
import tkinter as tk
from tkinter import messagebox

from config import HOST, PORT, BUFFER_SIZE


IMAGE_MAP = {
    "keo": "images/keo.png",
    "bua": "images/bua.png",
    "bao": "images/bao.png"
}


class RPSClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keo - Bua - Bao")
        self.root.geometry("750x700")
        self.root.resizable(False, False)

        self.history = []
        self.has_played = False  # THEM BIEN KIEM TRA DA CHOI CHUA

        # ===== LOAD IMAGE =====
        self.images_small = {}
        self.images_big = {}

        for k, path in IMAGE_MAP.items():
            self.images_small[k] = tk.PhotoImage(file=path).subsample(2, 2)
            self.images_big[k] = tk.PhotoImage(file=path)

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
        btn_bottom.pack(fill="x", pady=15)

        tk.Button(
            btn_bottom,
            text="| |",
            font=("Arial", 12),
            width=4,
            command=self.pause_menu
        ).pack(side="right", padx=15)

        # ===== TIEU DE =====
        tk.Label(
            root,
            text="TRÒ CHƠI KÉO - BÚA - BAO",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # ===== TI SO =====
        tk.Label(
            root,
            text="TỈ SỐ",
            font=("Arial", 15, "bold")
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

        # CLIENT ICON (BÊN TRÁI)
        self.client_icon = tk.Label(icon_frame)
        self.client_icon.pack(side="left", padx=30)
        
        # KẾT QUẢ Ở GIỮA
        self.result_center = tk.Label(
            icon_frame,
            text="",
            font=("Arial", 30, "bold"),
            width=8
        )
        self.result_center.pack(side="left", padx=20)

        # SERVER ICON (BÊN PHẢI)
        self.server_icon = tk.Label(icon_frame)
        self.server_icon.pack(side="left", padx=30)

        # ===== LOI MOI CHOI (HIEN THI O GIUA) =====
        self.welcome_label = tk.Label(
            root,
            text="Mời bạn chơi !",
            font=("Arial", 30, "bold"),
            fg="black"
        )
        self.welcome_label.pack(pady=20)

        # ===== NUT CHON =====
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=25)

        for i, c in enumerate(["keo", "bua", "bao"]):
            tk.Button(
                btn_frame,
                image=self.images_small[c],
                width=80,
                height=80,
                command=lambda x=c: self.play(x)
            ).grid(row=0, column=i, padx=15)

    def play(self, choice):
        try:
            # AN LOI MOI CHOI SAU NUOC DI DAU TIEN
            if not self.has_played:
                self.welcome_label.pack_forget()
                self.has_played = True

            self.client_socket.send(choice.encode())
            result = json.loads(
                self.client_socket.recv(BUFFER_SIZE).decode()
            )

            if result["status"] == "ok":
                c = result["client_score"]
                s = result["server_score"]

                self.client_score_box.config(
                    text=str(result["client_score"])
                )
                self.server_score_box.config(
                    text=str(result["server_score"])
                )

                # HIEN THI HINH
                self.client_icon.config(
                    image=self.images_big[result["lua_chon_client"]]
                )
                self.server_icon.config(
                    image=self.images_big[result["lua_chon_server"]]
                )

                # HIEN THI MỘT KẾT QUẢ Ở GIỮA
                ket_qua_client = result['ket_qua'].upper()
                
                if ket_qua_client == "THANG":
                    self.result_center.config(text="THẮNG", fg="green")
                elif ket_qua_client == "THUA":
                    self.result_center.config(text="THUA", fg="red")
                else:
                    self.result_center.config(text="HÒA", fg="orange")

                # LUU LICH SU
                self.history.append({
                    "client": result["lua_chon_client"],
                    "server": result["lua_chon_server"],
                    "ket_qua": result["ket_qua"],
                    "client_score": c,
                    "server_score": s
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
            text="TẠM DỪNG GAME",
            font=("Arial", 12, "bold")
        ).pack(pady=15)

        tk.Button(
            pause_window,
            text="LỊCH SỬ",
            width=15,
            command=self.show_history
        ).pack(pady=5)

        tk.Button(
            pause_window,
            text="TIẾP TỤC",
            width=15,
            command=pause_window.destroy
        ).pack(pady=5)

        tk.Button(
            pause_window,
            text="THOÁT",
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
        history_window.geometry("420x320")
        history_window.resizable(False, False)

        self.pause_window.grab_release()
        history_window.grab_set()

        text = tk.Text(
            history_window,
            height=12,
            font=("Consolas", 10)
        )
        text.pack(padx=5, pady=5, fill="both")

        # ===== HEADER =====
        header = (
            "  Ván  |  Client  |  Server  |    KQ    |  Tỉ số\n"
            "-------+----------+----------+----------+---------\n"
        )
        text.insert("end", header)

        # ===== DATA =====
        for i, h in enumerate(self.history, start=1):
            text.insert(
                "end",
                f"   {i:<3} |   "
                f" {h['client']:<6}|    "
                f"{h['server']:<6}| "
                f"  {h['ket_qua']:<5}  |   "
                f"{h['client_score']}-{h['server_score']}\n"
            )

        text.pack(padx=5, pady=5, side="top", fill="x")

        tk.Button(
            history_window,
            text="QUAY LẠI",
            width=12,
            command=history_window.destroy
        ).pack(pady=0, side="top")

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