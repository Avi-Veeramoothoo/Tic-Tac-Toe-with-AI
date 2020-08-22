#
#
# _____________________________________________________________________________________________
# _____________________________________________________________________________________________
# STAGE 2
# _____________________________________________________________________________________________
# _____________________________________________________________________________________________
#
#

from random import randint


# initialize an empty board
board =[["_", "_", "_"],
         ["_", "_", "_"],
         ["_", "_", "_"]]

# print the board
def print_board(board):
    print('---------')
    for row in board:
        print('| ', end='')
        print(' '.join(row), end='')
        print(' |')
    print('---------')

# clear board template
def clear_board(board):
    for i in range(3):
         for j in range(3):
                  board[j][i] = " "
    return board

# update board with user move
def update_board(board):
    user = input("Enter the coordinates: ").split()
    if (len(user[0]) > 1):
        print("You should enter numbers!")
        return update_board(board)
    x = int(user[0])
    y = int(user[1])
    if (x < 1 or x > 3) or (y < 1 or y > 3):
        print("Coordinates should be from 1 to 3!")
        return update_board(board)
    if not (board[3 - y][x - 1] == " "):
        print("This cell is occupied! Choose another one!")
        return update_board(board)
    board_list = "".join([cell for row in board for cell in row ])
    if board_list.count("X") > board_list.count("O"):
        board[3 - y][x - 1] = "O"
    else:
        board[3 - y][x - 1] = "X"
    return board

# computer play easy
def play_easy(board):
    print('Making move level "easy"')
    x = randint(1, 3)
    y = randint(1, 3)
    if (x < 1 or x > 3) or (y < 1 or y > 3):
        return play_easy(board)
    if not (board[3 - y][x - 1] == " "):
        return play_easy(board)
    board_list = "".join([cell for row in board for cell in row ])
    if board_list.count("X") > board_list.count("O"):
        board[3 - y][x - 1] = "O"
    else:
        board[3 - y][x - 1] = "X"
    return board

# print state of game
def game_state(board):
    def row_count(letter, limit):
        return [(board[i].count(letter) == limit) for i in range(3)]
    lr_diagonal = [board[i][i] for i in range(3)]
    rl_diagonal = [board[2 - i][i] for i in range(3)]
    def diagonal_count(letter, limit):
        return (lr_diagonal.count(letter) == limit) or (rl_diagonal.count(letter) == limit)
    if (all(row_count(" ", 0))):
        print("Draw")
    elif (any(row_count("O", 3)) or diagonal_count("O", 3)):
        print("O wins")
    elif (any(row_count("X", 3)) or diagonal_count("X", 3)):
        print("X wins")
    else:
        print("Game not finished")

# play game
def easy_mode(board):
    board = clear_board(board)
    print_board(board)
    board = update_board(board)
    print_board(board)
    board = play_easy(board)
    print_board(board)

# run script
easy_mode(board)