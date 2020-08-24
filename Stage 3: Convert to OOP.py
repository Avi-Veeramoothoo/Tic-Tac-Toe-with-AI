#
#
# _____________________________________________________________________________________________
# _____________________________________________________________________________________________
# STAGE 3
# _____________________________________________________________________________________________
# _____________________________________________________________________________________________
#
#


from random import randint


class Game():
    START = "start"
    EXIT = "exit"
    USER = "user"
    EASY = "easy"
    PLAYER1 = "player1"
    PLAYER2 = "player2"
    DRAW = "Draw"
    O_WINS = "O wins"
    X_WINS = "X wins"
    GAME_NOT_FINISHED = "Game not finished"


# declare instance attributes 
    def __init__(self):
        self.command = None
        self.player1 = None
        self.player2 = None
        self.next_player = None
        self.state = Game.GAME_NOT_FINISHED
        self.board =[["_", "_", "_"],
                     ["_", "_", "_"],
                     ["_", "_", "_"]]

        
# clear board
    def clear_board(self):
        for i in range(3):
            for j in range(3):
                self.board[j][i] = " "

                
# print board
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


    def game_state(self):
        def line_check(board, letter, limit):
            return [(board[i].count(letter) == limit) for i in range(3)]

        lr_diagonal = [self.board[i][i] for i in range(3)]
        rl_diagonal = [self.board[2 - i][i] for i in range(3)]

        def diagonal_count(letter, limit):
            return (lr_diagonal.count(letter) == limit) or (rl_diagonal.count(letter) == limit)

        transposed_board = [[row[i] for row in self.board] for i in range(3)]

        if (any(line_check(self.board, "O", 3)) or any(line_check(transposed_board, "O", 3)) or diagonal_count("O", 3)): #
            return Game.O_WINS
        elif (any(line_check(self.board, "X", 3)) or any(line_check(transposed_board, "X", 3)) or diagonal_count("X", 3)): #
            return Game.X_WINS
        elif (all(line_check(self.board, " ", 0))):
            return Game.DRAW
        else:
            return Game.GAME_NOT_FINISHED


    def user_move(self):
        user = input("Enter the coordinates: ").split()
        if (len(user[0]) > 1):
            print("You should enter numbers!")
            return self.user_move()
        x = int(user[0])
        y = int(user[1])
        if (x < 1 or x > 3) or (y < 1 or y > 3):
            print("Coordinates should be from 1 to 3!")
            return self.user_move()
        if not (self.board[3 - y][x - 1] == " "):
            print("This cell is occupied! Choose another one!")
            return self.user_move()
        board_list = "".join([cell for row in self.board for cell in row])
        if board_list.count("X") > board_list.count("O"):
            self.board[3 - y][x - 1] = "O"
        else:
            self.board[3 - y][x - 1] = "X"


    def play_easy(self):
        x = randint(1, 3)
        y = randint(1, 3)
        if (x < 1 or x > 3) or (y < 1 or y > 3):
            return self.play_easy()
        if not (self.board[3 - y][x - 1] == " "):
            return self.play_easy()
        board_list = "".join([cell for row in self.board for cell in row])
        if board_list.count("X") > board_list.count("O"):
            self.board[3 - y][x - 1] = "O"
        else:
            self.board[3 - y][x - 1] = "X"
        print('Making move level "easy"')


    def next_move(self, player):
        if player == Game.USER:
            self.user_move()
        else:
            self.play_easy()


    def play(self):
        self.next_player = Game.PLAYER1
        while self.state == Game.GAME_NOT_FINISHED:
            if self.next_player == Game.PLAYER1:
                self.next_move(self.player1)
                self.print_board()
                self.state = self.game_state()
                self.next_player = Game.PLAYER2
            else:
                self.next_move(self.player2)
                self.print_board()
                self.state = self.game_state()
                self.next_player = Game.PLAYER1
        print(self.state, "\n")


    def menu(self, user_input):
        if self.valid_input(user_input):
            while self.command == Game.START:
                self.clear_board()
                self.print_board()
                self.play()
                user_input = input("Input command: ")
                self.menu(user_input)
        else:
            self.menu(input())

# run script
game = Game()
game.menu(input())

