from random import randint
import os

version = "v0.2.0-prototype"

if os.name == "nt": # checking for windows system to fix coloring
    os.system('')

RESET = "\033[0m"
COLORS = {
    "1": "\033[94m",        # light-blue
    "2": "\033[32m",        # green
    "3": "\033[91m",        # red
    "4": "\033[34m",        # dark-blue
    "5": "\033[31m",        # dark-red
    "6": "\033[36m",        # cyan
    "7": "\033[35m",        # magenta
    "8": "\033[90m",        # gray
    "!": "\033[43;30;1m",   # idk i lazy to check the color
    "*": "\033[41;97;1m",
    "_": "\033[90m",
    ".": "\033[37m",
    "BORDER": "\033[33m"
}


class Cell():
    def __init__(self, is_open:bool = False, is_flag:bool = False, is_mine:bool = False, nearby_mines:int = 0):
        self.is_open = is_open
        self.is_flag = is_flag
        self.is_mine = is_mine
        self.nearby_mines = nearby_mines

class SelectError(Exception):
    pass

def create_board():
    selecting = True
    while selecting: # doing some work
        print("Select board scale: ")
        print("1 - 9x9")
        print("2 - 16x16")
        print("3 - 16x30")
        print("4 - Select your own...")
        mode_select = input("Select mode: ")
        try:
            if mode_select == "1":
                rows, cols, mines = 9, 9, 10
                selecting = False
            elif mode_select == "2":
                rows, cols, mines = 16, 16, 40
                selecting = False
            elif mode_select == "3":
                rows, cols, mines = 16, 30, 99
                selecting = False
            elif mode_select == "4":
                try:
                    rows = int(input("Rows: "))
                    cols = int(input("Cols: "))
                    mines = int(input("Mines: "))
                    if (mines >= ((rows * cols) - 9)) or (rows < 4) or (cols < 4) or (mines < 1):
                        print("Incorrect settings! Setting to default...")
                        rows, cols, mines = 9, 9, 10
                    selecting = False
                except ValueError:
                    print("Incorrect input! Setting to default...")
                    rows, cols, mines = 9, 9, 10
                    selecting = False
            else:
                raise SelectError
        except (SelectError):
            print("Incorrent input! Try again.")
    # ==============
    # creating board
    # ==============
    board = []
    for y in range(0, rows):
        row = [] # earlier was named rows_massiv
        for x in range(0, cols):
            row.append(Cell())
        board.append(row)
    # ==============
    # creating mines
    # ==============
    placed_mines = 0
    while placed_mines < mines:
        ry = randint(0, rows - 1)
        rx = randint(0, cols - 1)
        if not board[ry][rx].is_mine:
            board[ry][rx].is_mine = True
            placed_mines += 1
            for nny in range (-1, 2):
                for nnx in range (-1, 2):
                    if 0 <= ry - nny < rows and 0 <= rx - nnx < cols and not board[ry - nny][rx - nnx].is_mine:
                        board[ry - nny][rx - nnx].nearby_mines += 1
        board[ry][rx].nearby_mines = 0
    return rows, cols, mines, board

def interact(rows, cols, board, moves):
    try:
        row = int(input("Row: "))
        col = int(input("Col: "))
        opt = input("Open/flag (op/fl): ")
        if 0 <= row - 1 < rows and 0 <= col - 1 < cols:
            if opt == "fl":
                board[row-1][col-1].is_flag = not board[row-1][col-1].is_flag
            elif opt == "op":
                if not board[row-1][col-1].is_flag:
                    board[row-1][col-1].is_open = True
                    if board[row-1][col-1].nearby_mines == 0:
                        queue = [(row - 1, col - 1)]
                        while queue:
                            cy, cx = queue.pop(0)
                            for dy in range(-1, 2):
                                for dx in range(-1, 2):
                                    ny, nx = cy + dy, cx + dx
                                    if 0 <= ny < rows and 0 <= nx < cols:
                                        neighbor = board[ny][nx]
                                        if not neighbor.is_open and not neighbor.is_flag:
                                            neighbor.is_open = True
                                            if neighbor.nearby_mines == 0:
                                                queue.append((ny, nx))
                else:
                    print("This cell is flagged!")
            else:
                raise ValueError
        else:
            raise ValueError
    except ValueError:
        print("Incorrect input! Try again.")

def checking(rows, cols, mines, board):
    win, lose = False, False
    nonmines_open = rows * cols - mines
    counted = 0
    for y in range(0, rows):
        for x in range(0, cols):
            if board[y][x].is_open and board[y][x].is_mine:
                lose = True
                return win, lose
            if board[y][x].is_open and not board[y][x].is_mine:
                counted += 1
    if counted == nonmines_open:
        win = True
        return win, lose
    else:
        return False, False




def print_board(rows, cols, board):
    print("   ", end="")
    for x in range(0, cols):
        if x + 1 < 10:
            print(f"{COLORS['BORDER']}{x + 1} {RESET}", end="")
        else:
            print(f"{COLORS['BORDER']}{x + 1}{RESET}", end="")
    print()

    for y in range(0, rows):
        row_toprint = []
        for x in range(0, cols):
            cell = board[y][x]
            if cell.is_flag:
                row_toprint.append(f"{COLORS['!']}!{RESET}")
            elif not cell.is_open:
                row_toprint.append(f"{COLORS['_']}_{RESET}")
            elif cell.is_mine:
                row_toprint.append(f"{COLORS['*']}*{RESET}")
            elif cell.nearby_mines > 0:
                num = str(cell.nearby_mines)
                row_toprint.append(f"{COLORS[num]}{num}{RESET}")
            else:
                row_toprint.append(f"{COLORS['.']}.{RESET}")
        print(f"{COLORS['BORDER']}{y + 1:2}{RESET} " + " ".join(row_toprint))

def main():
    print("Welcome to {KylVorn: 0xMines} Python prototype!")
    print(f"Version {version}")
    moves = 0
    rows, cols, mines, board = create_board()
    while True:
        print_board(rows, cols, board)
        interact(rows, cols, board, moves)
        win, lose = checking(rows, cols, mines, board)
        if lose:
            print_board(rows, cols, board)
            print("You lose!")
            break
        elif win:
            print_board(rows, cols, board)
            print("You win!")
            break


if __name__ == "__main__":
    main()