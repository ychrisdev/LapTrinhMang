# server/room.py
from game_logic import create_board

class Room:
    def __init__(self, size):
        self.size = size
        self.players = []
        self.board = create_board(size)
        self.turn = 0          # 0: X, 1: O
        self.finished = False  # ván đã kết thúc chưa

    def add_player(self, conn):
        if len(self.players) < 2:
            self.players.append(conn)

    def is_full(self):
        return len(self.players) == 2

    def current_player(self):
        return self.players[self.turn]

    def switch_turn(self):
        self.turn = 1 - self.turn

    def get_symbol(self, conn):
        return "X" if self.players[0] == conn else "O"

    def reset(self):
        self.board = create_board(self.size)
        self.turn = 0
        self.finished = False
