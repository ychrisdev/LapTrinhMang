# server/game_logic.py

def create_board(size):
    return [[None for _ in range(size)] for _ in range(size)]

def check_win(board, x, y, symbol):
    size = len(board)

    def count(dx, dy):
        c = 0
        i = 1
        while True:
            nx = x + dx * i
            ny = y + dy * i
            if 0 <= nx < size and 0 <= ny < size and board[nx][ny] == symbol:
                c += 1
                i += 1
            else:
                break
        return c

    # 4 hướng: ngang, dọc, chéo \
    # và chéo /
    directions = [(1,0), (0,1), (1,1), (1,-1)]

    for dx, dy in directions:
        total = 1 + count(dx, dy) + count(-dx, -dy)
        if total >= (3 if size == 3 else 5):
            return True

    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True
