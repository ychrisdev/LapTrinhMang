from game_logic import create_board

class Room:
    def __init__(self, size):
        self.size = size
        self.players = []
        self.board = create_board(size)
        self.turn = 0
        self.finished = False
        self.rematch_votes = {}
        self.paused_by = set()

    def add_player(self, conn):
        if len(self.players) < 2:
            self.players.append(conn)
            self.rematch_votes[conn] = False

    def current_player(self):
        return self.players[self.turn]

    def switch_turn(self):
        self.turn = 1 - self.turn

    def get_symbol(self, conn):
        return "X" if self.players[0] == conn else "O"

    def reset_votes(self):
        for p in self.players:
            self.rematch_votes[p] = False

    def is_paused(self):
        return len(self.paused_by) > 0

    def reset(self):
        self.board = create_board(self.size)
        self.turn = 0
        self.finished = False
        self.paused_by.clear()