#
#
# _____________________________________________________________________________________________
# _____________________________________________________________________________________________
# STAGE 5
# _____________________________________________________________________________________________
# _____________________________________________________________________________________________
#
#
import math
from random import randint


class Game:
    START = "start"
    EXIT = "exit"
    USER = "user"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    TURN1 = "turn1"
    TURN2 = "turn2"
    EMPTY_CELL = " "
    X_Move = "X"
    O_Move = "O"
    DRAW = "Draw"
    X_WINS = "X wins"
    O_WINS = "O wins"
    GAME_NOT_FINISHED = "Game not finished"

    # declare instance attributes
    def __init__(self):
        self.command = None
        self.player1 = None
        self.player2 = None
        self.next_turn = None
        self.x_coord = None
        self.y_coord = None
        self.state = Game.GAME_NOT_FINISHED
        self.board = [["_", "_", "_"],
                      ["_", "_", "_"],
                      ["_", "_", "_"]]  # initialize an empty board

    # clear board template
    def clear_board(self):
        for i in range(3):
            for j in range(3):
                self.board[j][i] = " "

    # print the board
    def print_board(self):
        print('---------')
        for row in self.board:
            print('| ', end='')
            print(' '.join(row), end='')
            print(' |')
        print('---------')

    # determine if user input is valid
    def valid_input(self, args):
        user_input = args.split()
        if (len(user_input) == 1 and user_input[0] == Game.EXIT):
            self.command = Game.EXIT
            return True
        elif (len(user_input) == 3 and user_input[0] == Game.START):
            self.command = user_input[0]
            self.player1 = user_input[1]
            self.player2 = user_input[2]
            return True
        else:
            print("Bad parameters!")
            return False

    # determine and return game state: win, lose, draw or unfinished
    def game_state(self, board):
        def line_check(board, letter, limit):
            return [(board[i].count(letter) == limit) for i in range(3)]

        lr_diagonal = [board[i][i] for i in range(3)]
        rl_diagonal = [board[2 - i][i] for i in range(3)]

        def diagonal_count(letter, limit):
            return (lr_diagonal.count(letter) == limit) or (rl_diagonal.count(letter) == limit)

        transposed_board = [[row[i] for row in board] for i in range(3)]

        def check_win(move, limit):
            if (any(line_check(board, move, limit))
                    or any(line_check(transposed_board, move, limit))
                    or diagonal_count(move, limit)):
                return True

        if check_win(Game.X_Move, 3):
            return Game.X_WINS
        elif check_win(Game.O_Move, 3):
            return Game.O_WINS
        elif all(line_check(board, Game.EMPTY_CELL, 0)):
            return Game.DRAW
        else:
            return Game.GAME_NOT_FINISHED

    def active_move(self):
        board_string = "".join([cell for row in self.board for cell in row])
        if board_string.count("X") > board_string.count("O"):
            return Game.O_Move
        else:
            return Game.X_Move


    def opponent_move(self):
        if self.active_move() == Game.X_Move:
            return Game.O_Move
        else:
            return Game.X_Move


    def update_board(self, x, y):
        self.board[3 - y][x - 1] = self.active_move()
        return True

    # update board template with valid user move
    def user_move(self):
        coord = input("Enter the coordinates: ").split()
        if not (coord[0].isnumeric() and coord[1].isnumeric()):
            print("You should enter numbers!")
            return self.user_move()
        x = int(coord[0])
        y = int(coord[1])
        if (x < 1 or x > 3) or (y < 1 or y > 3):
            print("Coordinates should be from 1 to 3!")
            return self.user_move()
        if not (self.board[3 - y][x - 1] == Game.EMPTY_CELL):
            print("This cell is occupied! Choose another one!")
            return self.user_move()
        self.update_board(x, y)

    # update board template with valid computer move on Easy Mode
    def play_random(self):
        x = randint(1, 3)
        y = randint(1, 3)
        if not (self.board[3 - y][x - 1] == Game.EMPTY_CELL):
            return self.play_random()
        self.update_board(x, y)

    def easy_move(self):
        self.play_random()
        print('Making move level "easy"')

    def play_smart(self):
        board_list = [cell for row in self.board for cell in row]
        empty_cells_index = [i for i in range(len(board_list)) if board_list[i] == Game.EMPTY_CELL]
        for index in empty_cells_index:
            self.board[index // 3][index % 3] = self.active_move()
            if self.game_state(self.board) == Game.X_WINS or self.game_state(self.board) == Game.O_WINS:
                return True
            else:
                self.board[index // 3][index % 3] = Game.EMPTY_CELL
        for index in empty_cells_index:
            self.board[index // 3][index % 3] = self.opponent_move()
            if self.game_state(self.board) == Game.X_WINS or self.game_state(self.board) == Game.O_WINS:
                self.board[index // 3][index % 3] = self.active_move()
                return True
            else:
                self.board[index // 3][index % 3] = Game.EMPTY_CELL
                return False

    def medium_move(self):
        if self.play_smart():
            pass
        else:
            self.play_random()
        print('Making move level "medium"')


    def minimax(self, is_ai_turn, active_move, board):
        if self.game_state(board) == Game.DRAW:
            return 0
        elif self.game_state(board) == Game.X_WINS:
            return 1 if is_ai_turn else -1
        elif self.game_state(board) == Game.O_WINS:
            return 1 if is_ai_turn else -1

        def reverse_mark(ai_mark):
            return "X" if ai_mark == "O" else "O"

        scores = []
        board_list = [cell for row in board for cell in row]
        empty_cells_index = [i for i in range(len(board_list)) if board_list[i] == Game.EMPTY_CELL]
        for index in empty_cells_index:
            board[index // 3][index % 3] = active_move
            scores.append(self.minimax(not is_ai_turn, reverse_mark(active_move), board))
            board[index // 3][index % 3] = Game.EMPTY_CELL
        return max(scores) if is_ai_turn else min(scores)


    def hard_move(self):
        best_score = -math.inf
        best_index = None

        board_list = [cell for row in self.board for cell in row]
        empty_cells_index = [i for i in range(len(board_list)) if board_list[i] == Game.EMPTY_CELL]
        for index in empty_cells_index:
            self.board[index // 3][index % 3] = self.active_move()
            score = self.minimax(False, self.opponent_move(), self.board)
            self.board[index // 3][index % 3] = Game.EMPTY_CELL
            if score > best_score:
                best_score = score
                best_index = index
        print('Making move level "hard"')
        self.board[best_index // 3][best_index % 3] = self.active_move()


    # determine next player level and initiate move
    def next_move(self, level):
        if level == Game.USER:
            self.user_move()
        elif level == Game.EASY:
            self.easy_move()
        elif level == Game.MEDIUM:
            self.medium_move()
        elif level == Game.HARD:
            self.hard_move()

    # play game
    def play(self):
        self.next_turn = Game.TURN1
        while self.state == Game.GAME_NOT_FINISHED:
            if self.next_turn == Game.TURN1:
                self.next_move(self.player1)
                self.next_turn = Game.TURN2
            else:
                self.next_move(self.player2)
                self.next_turn = Game.TURN1
            self.print_board()
            self.state = self.game_state(self.board)
        print(self.state, "\n")


    # game menu to decide user action: start, re-start or exit game
    def menu(self, user_input):
        if self.valid_input(user_input):
            while self.command == Game.START:
                self.clear_board()
                self.print_board()
                self.play()
                self.state = Game.GAME_NOT_FINISHED
                self.menu(input("Input command: "))
        else:
            self.menu(input("Input command: "))


#run script
game = Game()
game.menu(input())

