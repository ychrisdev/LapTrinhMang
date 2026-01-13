import tkinter as tk
from ui_menu import MenuScreen
from ui_game import GameScreen

class App(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.title("Caro Game")
        self.geometry("600x700")
        self.resizable(False, False)

        self.client = client
        self.current_screen = None
        
        self.score = {"me": 0, "op": 0}
        
        self.show_menu()
        self.is_leaving = False

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None

    def show_menu(self):
        self.clear_screen()
        self.current_screen = MenuScreen(self, self.client)
        self.current_screen.pack(fill="both", expand=True)

    def handle_message(self, msg):
        msg_type = msg["type"]
        data = msg["data"]

        if msg_type == "waiting":
            if hasattr(self.current_screen, "set_status"):
                self.current_screen.set_status(data["message"])

        elif msg_type == "start_game":
            self.clear_screen()
            self.current_screen = GameScreen(
                self,
                self,
                data["size"],
                data["symbol"],
                data["your_turn"],
                score=self.score      # 🔥 LẤY SCORE TỪ APP
            )
            self.current_screen.pack(fill="both", expand=True)


        elif msg_type == "update":
            if hasattr(self.current_screen, "handle_update"):
                self.after(0, lambda: self.current_screen.handle_update(
                    data["x"], data["y"], data["symbol"]
                ))

        elif msg_type == "win":
            if hasattr(self.current_screen, "handle_win"):
                self.after(0, lambda: self.current_screen.handle_win(data["winner"]))

        elif msg_type == "draw":
            if hasattr(self.current_screen, "handle_draw"):
                self.after(0, self.current_screen.handle_draw)

        elif msg_type == "opponent_pause":
            if hasattr(self.current_screen, "handle_opponent_pause"):
                self.after(0, self.current_screen.handle_opponent_pause)

        elif msg_type == "opponent_resume":
            if hasattr(self.current_screen, "handle_opponent_resume"):
                self.after(0, self.current_screen.handle_opponent_resume)


        elif msg_type == "back_to_menu":
            self.score = {"me": 0, "op": 0}
            if isinstance(self.current_screen, GameScreen):
                if self.is_leaving:
                    self.is_leaving = False
                    self.show_menu()
                    return

                try:
                    self.current_screen.status.config(
                        text="Đối thủ đã thoát ván đấu",
                        fg="red"
                    )
                    self.after(3000, self.show_menu)
                    return
                except:
                    pass

            self.show_menu()
