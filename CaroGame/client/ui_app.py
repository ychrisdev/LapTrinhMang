# client/ui_app.py
import tkinter as tk
from ui_menu import MenuScreen
from ui_game import GameScreen

class App(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.title("Caro Online")
        self.geometry("600x700")
        self.resizable(False, False)

        self.client = client
        self.current_screen = None

        self.show_menu()

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

        if msg_type == "start_game":
            # Chuyển sang màn hình chơi
            self.clear_screen()
            self.current_screen = GameScreen(
                self,
                self,
                data["size"],
                data["symbol"],
                data["your_turn"]
            )
            self.current_screen.pack(fill="both", expand=True)

        elif msg_type == "update":
            if hasattr(self.current_screen, "handle_update"):
                self.current_screen.handle_update(
                    data["x"], data["y"], data["symbol"]
                )

        elif msg_type == "win":
            if hasattr(self.current_screen, "handle_win"):
                self.current_screen.handle_win(data["winner"])

        elif msg_type == "draw":
            if hasattr(self.current_screen, "handle_draw"):
                self.current_screen.handle_draw()

        elif msg_type == "back_to_menu":
            self.show_menu()
