# doing some minesweeper on python
# ngl my english level is not good but i will comment in english to practice
from random import randint

board = []
selected = False
win = False
lose = False
game = True
class SelectError(Exception): # for open_cell()
    pass

class Cell:
    def __init__(self, is_mine:bool = False, is_open:bool = False, is_flag:bool = False, nearby_mines:int = 0):
        self.is_mine = is_mine
        self.is_open = is_open
        self.is_flag = is_flag
        self.nearby_mines = nearby_mines


def create_board(rows:int, cols:int, mines:int):
    total_mines = 0
    for y in range(0, rows): # creating cells
        row = []
        for x in range(0, cols):
            row.append(Cell())
        board.append(row)
    while total_mines < mines: # creating mines
        ry = randint(0, rows - 1)
        rx = randint(0, cols - 1)
        if not board[ry][rx].is_mine:
            board[ry][rx].is_mine = True
            #board[ry][rx].is_open = True # for debugging
            total_mines += 1
            for e in range (-1, 2):
                for q in range(-1, 2):
                    if 0 <= ry - q < rows and 0 <= rx - e < cols and not board[ry - q][rx - e].is_mine:
                        board[ry - q][rx - e].nearby_mines += 1
            board[ry][rx].nearby_mines = 0

def open_cell(): # opening cels
    global lose, game
    while game:
        print_board()
        print("Select cell:")
        try:
            row = int(input("Input row: ")) - 1
            col = int(input("Input col: ")) - 1
            if row < 0 or col < 0:
                raise IndexError
            print("Do you want to flag cell or open it?")
            open_type = input("Input (fl/op): ")
            if not (open_type == "fl") and not (open_type == "op"):
                raise SelectError
            elif open_type == "fl":
                board[row][col].is_flag = not board[row][col].is_flag
            elif open_type == "op":
                if board[row][col].is_flag:
                    print("Cell is flagged!")
                    continue
                board[row][col].is_open = True
                if board[row][col].is_mine == True:
                    lose = True
                    game = False
        except (ValueError, SelectError, IndexError):
            print("Incorrect input! Try again.")
            continue
        check_win()


def print_board():
    for y in range(0, rows):
        print_str = []
        for x in range(0, cols):
            cell = board[y][x]
            if cell.is_flag:
                print_str.append("!")
            elif not cell.is_open:
                print_str.append("_")
            elif cell.is_mine:
                print_str.append("*")
            else:
                print_str.append(cell.nearby_mines if cell.nearby_mines > 0 else ".")
        print(" ".join(map(str, print_str)))

def check_win():
    global win, lose, game
    total_cells = rows*cols
    checked_forwin = 0
    for row in range(0, rows):
        for col in range(0, cols):
            if not lose:
                if board[row][col].is_open and not board[row][col].is_mine:
                    checked_forwin += 1
    if checked_forwin == rows*cols-mines:
        win = True
        game = False


while True: # select menu
    print("Select mode")
    print("1 - Board 9x9")
    print("2 - Board 16x16")
    print("3 - Board 16x32")
    print("4 - Board XXxXX...")
    ans = input("Select your mode: ")
    if ans == "1":
        rows, cols, mines = 9, 9, 10
        break
    elif ans == "2":
        rows, cols, mines = 16, 16, 40
        break
    elif ans == "3":
        rows, cols, mines = 16, 32, 99
        break
    elif ans == "4":
        while not selected:
            try:
                rows = int(input("Rows: "))
                cols = int(input("Cols: "))
                mines = int(input("Mines: "))
                if (mines >= ((rows * cols) - 9)) or (rows < 4) or (cols < 4) or (mines < 1):
                    print("Incorrect settings! Setting default settings...")
                    rows, cols, mines = 9, 9, 10
            except ValueError:
                print("Incorrect input! Setting default settings...")
                rows, cols, mines = 9, 9, 10
            break
        break
    else:
        print("Incorrect input! Try again.")
create_board(rows, cols, mines)
print("The game starts.")
while True:
    if lose:
        print_board()
        print("You lose!")
        break
    elif win:
        print_board()
        print("You win!")
        break
    open_cell()