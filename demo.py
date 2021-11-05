import time
import threading
from tkinter import *
from tkinter import font
import math
import os
import importlib
import sys
from contextlib import suppress
import gc

from PIL import Image, ImageTk

import random

from copy import deepcopy

class Consts:
    TIMEOUT = 1
    THINK = 30
    DRAW = "DRAW"
    MAX_MOVES = 100

class EventPH:
    def __init__(self, widget):
        self.widget = widget

class WidgetPH:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Players:
    player1=None
    player2=None
    base1=None
    base2=None
    @staticmethod
    def load(file1, file2):
        Players.base1 = os.path.splitext(file1)[0]
        Players.base2 = os.path.splitext(file2)[0]
        try:
                mod1 = importlib.import_module(Players.base1)
                mod2 = importlib.import_module(Players.base2)
                Players.player1 = getattr(mod1, Players.base1)
                Players.player2 = getattr(mod2, Players.base2)
#                result = method_to_call(5)
        except (RuntimeError, TypeError, NameError,Exception):
                print(NameError) 
                return False
        
        return True


    def find_all(directory):
        sys.path.insert(0, directory)
        counter = 0
        cands = []
        for file in os.listdir(directory):
            cands.append(file)
        return cands       

class Board_2players():
    def __init__(self, master, game, player, computer):

        self.currently_highlighted = []
        if computer == "black":
            self.current_turn = player

        else:
            self.current_turn = computer
        self.game = game
        self.player = player
        self.computer = computer
        self.window = master

        self.all_buttons = []
        self.open_images()
        self.build_board(master)

    def open_images(self):
        self.black_cell = Image.open("images/black_cell.jpg")
        self.black_cell.thumbnail((75, 75))
        self.black_cell = ImageTk.PhotoImage(self.black_cell)

        self.white_cell = Image.open("images/white_cell.jpg")
        self.white_cell.thumbnail((75, 75))
        self.white_cell = ImageTk.PhotoImage(self.white_cell)

        self.black_queen = Image.open("images/b_q.jpg")
        self.black_queen.thumbnail((75, 75))
        self.black_queen = ImageTk.PhotoImage(self.black_queen)

        self.white_queen = Image.open("images/w_q.jpg")
        self.white_queen.thumbnail((75, 75))
        self.white_queen = ImageTk.PhotoImage(self.white_queen)

        self.black_piece = Image.open("images/b_p.jpg")
        self.black_piece.thumbnail((75, 75))
        self.black_piece = ImageTk.PhotoImage(self.black_piece)

        self.white_piece = Image.open("images/w_p.jpg")
        self.white_piece.thumbnail((75, 75))
        self.white_piece = ImageTk.PhotoImage(self.white_piece)

        self.highlighted_cell = Image.open("images/h_c.jpg")
        self.highlighted_cell.thumbnail((75, 75))
        self.highlighted_cell = ImageTk.PhotoImage(self.highlighted_cell)

        self.highlighted_wqueen = Image.open("images/h_w_q.jpg")
        self.highlighted_wqueen.thumbnail((75, 75))
        self.highlighted_wqueen = ImageTk.PhotoImage(self.highlighted_wqueen)

        self.highlighted_wpiece = Image.open("images/h_w.jpg")
        self.highlighted_wpiece.thumbnail((75, 75))
        self.highlighted_wpiece = ImageTk.PhotoImage(self.highlighted_wpiece)

        self.highlighted_bqueen = Image.open("images/h_b_q.jpg")
        self.highlighted_bqueen.thumbnail((75, 75))
        self.highlighted_bqueen = ImageTk.PhotoImage(self.highlighted_bqueen)

        self.highlighted_bpiece = Image.open("images/h_b.jpg")
        self.highlighted_bpiece.thumbnail((75, 75))
        self.highlighted_bpiece = ImageTk.PhotoImage(self.highlighted_bpiece)


    def endGame(self):
        self.window.quit()
        self.window.event_generate("<<Foo>>", when="tail")

    def newGame(self, event, master):
        master.destroy()
        root = Tk()
        root.title('Checkers')
        Game_2players(root, "white", "black")
        root.mainloop()

    def build_board(self, master):
        frame = Frame(master)
        newfont = font.Font(size=30)
        title = Players.base1 + " VS " + Players.base2
        restart = Button(frame, text=title, fg="green")
        restart['font'] = newfont
        restart.pack(side=LEFT)
        restart.bind("<Button-1>", lambda event, root=master: self.newGame(event, master))

        for row in range(0, 8, 1):
            for col in range(0, 8, 1):
                b = Button(master)
                if row%2 == 0:
                    if col%2 == 0:
                        b.image = self.black_cell
                    else:
                        b.image = self.white_cell
                else:
                    if col%2 == 1:
                        b.image = self.black_cell
                    else:
                        b.image = self.white_cell

                b["image"] = b.image
                b.color = "no color"
                b.highlighted = self.highlighted_cell
                b.row = row
                b.col = col
                b.bind("<Button-1>", self.game.possible_placing)
                b.grid(column=col, row=row)
                self.all_buttons.append(b)

        frame.grid(row=8, columnspan=8, rowspan=3)


    def bind_placings_func(self, turn=""):
        if turn == "":
            for button in self.all_buttons:
                button.bind("<Button-1>", self.game.possible_placing)
        if turn == self.computer:
            for button in self.all_buttons:
                if button.color == self.computer:
                    button.bind("<Button-1>", self.game.possible_placing)
        if turn == self.player:
            for button in self.all_buttons:
                if button.color == self.player:
                    button.bind("<Button-1>", self.game.possible_placing)

    def unbind_placings_func(self, turn=""):
        if turn == "":
            for button in self.all_buttons:
                button.unbind("<Button-1>")
        if turn == self.computer:
            for button in self.all_buttons:
                if button.color == self.computer:
                    button.unbind("<Button-1>")
        if turn == self.player:
            for button in self.all_buttons:
                if button.color == self.player:
                    button.unbind("<Button-1>")

    def update_old_cell(self, old_coord):
        for button in self.all_buttons:
            if button.row == old_coord[0] and button.col == old_coord[1]:
                button.image = self.black_cell
                button.highlighted = self.highlighted_cell
                button['image'] = button.image
                button.color = "no color"
                button.row = old_coord[0]
                button.col = old_coord[1]

    def show(self, board, nextCapture = [False, ""]):
        button_list_counter = 0
        for row in board:
            for piece in row:
                if piece != None:
                    if piece.color == "black":
                        if piece.isQueen:
                            self.all_buttons[button_list_counter].image = self.black_queen
                            self.all_buttons[button_list_counter].highlighted = self.highlighted_bqueen
                        else:
                            self.all_buttons[button_list_counter].image = self.black_piece
                            self.all_buttons[button_list_counter].highlighted = self.highlighted_bpiece
                        self.all_buttons[button_list_counter].color = "black"
                    elif piece.color == "white":
                        if piece.isQueen:
                            self.all_buttons[button_list_counter].image = self.white_queen
                            self.all_buttons[button_list_counter].highlighted = self.highlighted_wqueen
                        else:
                            self.all_buttons[button_list_counter].image = self.white_piece
                            self.all_buttons[button_list_counter].highlighted = self.highlighted_wpiece
                        self.all_buttons[button_list_counter].color = "white"
                    self.all_buttons[button_list_counter]["image"] = self.all_buttons[button_list_counter].image
                button_list_counter += 1
        self.bind_placings_func()
        self.unbind_placings_func(self.current_turn)

        if not nextCapture[0]:
            if self.current_turn == self.player:
                self.current_turn = self.computer
            else:
                self.current_turn = self.player
            self.game.capture_options(self.current_turn)
        if nextCapture[0]:
            self.game.multiple_capture(nextCapture[1], nextCapture[2], self.current_turn)

    def highlight(self, buttons, event):
        self.dehighlight(self.currently_highlighted)
        for coordinate in buttons:
            for button in self.all_buttons:
                if button.row == coordinate[0] and button.col == coordinate[1]:
                    button["image"] = button.highlighted
                    button.bind("<Button-1>", lambda new_cell, row = button.row, col = button.col: self.game.move(new_cell,row, col, event, buttons))
        event.widget["image"] = event.widget.highlighted
        buttons.append([event.widget.row, event.widget.col])
        self.currently_highlighted = buttons

    def highlight_to_eat(self, buttons, attackers):
        self.dehighlight(self.currently_highlighted)
        self.unbind_placings_func()
        for coordinate in buttons:
            for button in self.all_buttons:
                if button.row == coordinate[0] and button.col == coordinate[1]:
                    button["image"] = button.highlighted
                    button.bind("<Button-1>", lambda new_cell, row=button.row, col=button.col, attacker = coordinate[2]: self.game.eat(new_cell, row, col, attacker, buttons, self.current_turn))

        for coordinate in attackers:
            for button in self.all_buttons:
                if button.row == coordinate[0] and button.col == coordinate[1]:
                    button["image"] = button.highlighted
                    buttons.append([button.row, button.col])
        self.currently_highlighted = buttons


    def dehighlight(self, buttons):
        for coordinate in buttons:
            for button in self.all_buttons:
                if button.row == coordinate[0] and button.col == coordinate[1]:
                    button["image"] = button.image
                    #button.bind("<Button-1>", self.game.possible_placing)


class gamePiece():
    def __init__(self, row, col, isQueen, color):
        self.row = row
        self.col = col
        self.isQueen = isQueen
        self.color = color


    def canEat(self, row, col, board, turn, isQueen = False):
        '''
        function checks if one piece can capture another piece at [row][col]
        :param row: row
        :param col: column
        :param board: arr[][] of game board
        :param turn: current turn
        :param isQueen: is a piece a queen
        :return: True if can capture
                 False if cannot capture
        '''
        if row+1 > 7 or row-1 < 0 or col+1 > 7 or col-1 < 0 or board[row][col] == None or board[row][col].color == self.color:
            return False
        if turn == "player":
            if (not isQueen and self.row <= row):
                return False

            if self.row-1 >= 0:
                if col-1 == self.col and col+1 < 8:
                    if board[row-1][col+1] == None:
                        return True
                if col+1 == self.col and col-1 >= 0:
                    if board[row-1][col-1] == None:
                        return True

            if isQueen and row + 1 < 8:
                if col-1 == self.col and col+1 < 8:
                    if board[row+1][col+1] == None:
                        return True
                if col+1 == self.col and col-1 >= 0:
                    if board[row+1][col-1] == None:
                        return True

        if turn == "computer":
            if (not isQueen and self.row >= row):
                return False

            if self.row + 1 < 8:
                if col-1 == self.col and col + 1 < 8:
                    if board[row + 1][col + 1] == None:
                        return True
                if col+1 == self.col and col - 1 >= 0:
                    if board[row + 1][col - 1] == None:
                        return True

            if isQueen and row - 1 >= 0:
                if col-1 == self.col and col+1 < 8:
                    if board[row-1][col+1] == None:
                        return True
                if col+1 == self.col and col-1 >= 0:
                    if board[row-1][col-1] == None:
                        return True

        return False

    def possible_placing(self,game_board):
        placings = []

        isPlayer = True if (self.color == "white") else False
        if isPlayer:
            if self.row-1 >= 0:
                if self.col+1 < 8:
                    if game_board[self.row-1][self.col+1] == None:
                        placings.append([self.row-1, self.col+1])
                if self.col-1 >= 0:
                    if game_board[self.row-1][self.col-1] == None:
                        placings.append([self.row-1, self.col-1])
            if self.isQueen and self.row+1 < 8:
                if self.col+1 < 8:
                    if game_board[self.row+1][self.col+1] == None:
                        placings.append([self.row+1, self.col+1])
                if self.col-1 >= 0:
                    if game_board[self.row+1][self.col-1] == None:
                        placings.append([self.row+1, self.col-1])

        if not isPlayer:
            if self.row + 1 < 8:
                if self.col + 1 < 8:
                    if game_board[self.row + 1][self.col + 1] == None:
                        placings.append([self.row + 1, self.col + 1])
                if self.col - 1 >= 0:
                    if game_board[self.row + 1][self.col - 1] == None:
                        placings.append([self.row + 1, self.col - 1])
            if self.isQueen and self.row-1 >= 0:
                if self.col+1 < 8:
                    if game_board[self.row-1][self.col+1] == None:
                        placings.append([self.row-1,self. col+1])
                if self.col-1 >= 0:
                    if game_board[self.row-1][self.col-1] == None:
                        placings.append([self.row-1, self.col-1])        
        return placings

class Game_2players():
    def __init__(self, master, p_color, c_color):
        self.player = p_color
        self.computer = c_color
        self.game_board = self.starting_board()
        self.winner = ""
        self.move_no = 0
        self.last_move = (self.player,0,0)
        self.view = Board_2players(master, self, self.player, self.computer)
        timer = threading.Timer(Consts.TIMEOUT, lambda: self.make_move())
        timer.start()        
        self.view.show(self.game_board)


    def starting_board_test(self):             # creating starting game board
        gameBoard = []
        temp = []
        if self.player == "white":
            computer_color = "black"
        else:
            computer_color = "white"

        for i in range(0, 3, 1):    # filling first 3 rows with black pieces
            for j in range(0, 8, 1):
                if (i ==1 and j == 5):
                       temp.append(gamePiece(1, 5, False, self.player))
                       continue
                if i % 2 == 0:
                    if (i == 2 and j in(2,4)):
                        temp.append(gamePiece(i, j, False, computer_color))
                    elif j % 2 == 0:
#                        temp.append(gamePiece(i, j, False, computer_color))
                         temp.append(None)
                    else:
                        temp.append(None)
                else:
                    if (i == 1 and j == 3):
                        temp.append(gamePiece(i, j, False, computer_color))
                    elif j % 2 == 1:
#                        temp.append(gamePiece(i, j, False, computer_color))
                         temp.append(None)
                    else:
                        temp.append(None)
            gameBoard.append(temp)
            temp = []

        for i in range(3, 4, 1):     # filling two middle rows with "NONE"
            for j in range(0, 8, 1):
                temp.append(None)
            gameBoard.append(temp)
            temp = []

        for i in range(4, 8, 1):       # filling last 3 rows with white pieces
            for j in range(0, 8, 1):
                if i % 2 == 1:
                    if j % 2 == 1:
                        temp.append(gamePiece(i, j, False, self.player))
                    else:
                        temp.append(None)
                else:
                    if j % 2 == 0:
                        temp.append(gamePiece(i, j, False, self.player))
                    else:
                        temp.append(None)
            gameBoard.append(temp)
            temp = []

        return gameBoard

    def starting_board(self):             # creating starting game board
        gameBoard = []
        temp = []
        if self.player == "white":
            computer_color = "black"
        else:
            computer_color = "white"

        for i in range(0, 3, 1):    # filling first 3 rows with black pieces
            for j in range(0, 8, 1):
                if i % 2 == 0:
                    if j % 2 == 0:
                        temp.append(gamePiece(i, j, False, computer_color))
                    else:
                        temp.append(None)
                else:
                    if j % 2 == 1:
                        temp.append(gamePiece(i, j, False, computer_color))
                    else:
                        temp.append(None)
            gameBoard.append(temp)
            temp = []

        for i in range(3, 5, 1):     # filling two middle rows with "NONE"
            for j in range(0, 8, 1):
                temp.append(None)
            gameBoard.append(temp)
            temp = []

        for i in range(5, 8, 1):       # filling last 3 rows with white pieces
            for j in range(0, 8, 1):
                if i % 2 == 1:
                    if j % 2 == 1:
                        temp.append(gamePiece(i, j, False, self.player))
                    else:
                        temp.append(None)
                else:
                    if j % 2 == 0:
                        temp.append(gamePiece(i, j, False, self.player))
                    else:
                        temp.append(None)
            gameBoard.append(temp)
            temp = []

        return gameBoard

    def too_long_turn(self):
        winner = self.computer if (self.view.current_turn == self.player) else self.player
        self.winner = winner
        print("Too long turn for  " + self.view.current_turn + ". "+ winner + " is the winner")
        self.view.endGame()

    def update_options_for_location(self, i,j, game_board, color, turn, placings, eatings):
        if game_board[i][j] != None and  game_board[i][j].color == color:
            candiate_eatings = [(i+1,j+1), (i+1,j-1), (i-1,j+1), (i-1,j-1)]
            # eating has mandatory priority
            for eat in candiate_eatings:
                if game_board[i][j].canEat(eat[0], eat[1], game_board, turn, game_board[i][j].isQueen):
                    if ((i,j) not in eatings):
                            eatings[(i,j)] = []
                    eatings[(i,j)].append([eat[0]-i+eat[0], eat[1]-j+eat[1]])
            # if no eating lets check regular move
            if (len(eatings) == 0):
                options = game_board[i][j].possible_placing(game_board)
                if (len(options) > 0):
                    for k in range(len(options)):
                        placings[(i,j)]  = options

    def is_valid_move(self, player_move,start_at):
        placings = {}
        eatings = {}
        turn = "player" if (self.view.current_turn == "white") else "computer"

        if (start_at != None):
            i = start_at[0]
            j = start_at[1]
            self.update_options_for_location(i,j, self.game_board, self.view.current_turn, turn, placings, eatings)

        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                self.update_options_for_location(i,j, self.game_board, self.view.current_turn, turn, placings, eatings)

        if (len(eatings) > 0):
            array_to_use = eatings
        else:
            array_to_use = placings

        start = (player_move[0], player_move[1])
        end = [player_move[2], player_move[3]]
        if (( start in array_to_use) and (end in array_to_use[start])):
            return True

        return False

    def make_move(self):
        self.move_no = self.move_no + 1
        start_at = None
        pass_board = deepcopy(self.game_board)
        if (self.last_move[0] == self.view.current_turn):
            start_at = (self.last_move[1], self.last_move[2])
        
        long_turn_timer = threading.Timer(Consts.THINK+1, lambda: self.too_long_turn())
        long_turn_timer.start()    

        if (self.view.current_turn == self.computer):
            bestMove = Players.player1(pass_board, self.view.current_turn, self.move_no, Consts.THINK, start_at)
        else:
            bestMove = Players.player2(pass_board, self.view.current_turn, self.move_no, Consts.THINK, start_at)

        long_turn_timer.cancel()
        self.view.dehighlight(self.view.currently_highlighted)
        if (len(bestMove) > 0):
            if (not self.is_valid_move(bestMove,start_at)):
                print (self.view.current_turn + " made and illegal move. LOST!")
                winner = self.computer if (self.view.current_turn == self.player) else self.player
                self.winner = winner
                self.view.endGame()
                return                

        if (len(bestMove) == 0 or (start_at != None and (bestMove[0] != start_at[0] or bestMove[1] != start_at[1]))):
            winner = self.computer if (self.view.current_turn == self.player) else self.player
            self.winner = winner
            self.view.endGame()
            return
        
        if (self.move_no == Consts.MAX_MOVES):
            print ("Got to " + Consts.MAX_MOVES + ". Draw it is")
            self.winner = Consts.DRAW
            self.view.endGame()
            return            

        self.last_move = (self.view.current_turn, bestMove[2], bestMove[3])
        print(self.move_no, " move: ", bestMove)
        print("---------end turn----------")
        if abs(bestMove[2] - bestMove[0]) > 1 or abs(bestMove[3] - bestMove[1]) > 1:
            attacker = [bestMove[0], bestMove[1]]
            self.eat("", bestMove[2], bestMove[3], attacker, [], self.view.current_turn)
        else:
            self.move("", bestMove[2], bestMove[3], EventPH(WidgetPH(bestMove[0],bestMove[1])), [])
        timer = threading.Timer(Consts.TIMEOUT, lambda: self.make_move())
        timer.start()    

    def possible_placing(self, event):
        placings = []
        row = event.widget.row
        col = event.widget.col
        color = event.widget.color

        placings = self.game_board[row][col].possible_placing(self.game_board)
        self.view.highlight(placings, event)
        return 


    def toQueen(self, row, col):
        if row == 0 or row == 7:
            self.game_board[row][col].isQueen = True

    def move(self,new_cell, new_row, new_col,event, buttons):
        old_row = event.widget.row
        old_col = event.widget.col

        self.game_board[old_row][old_col].row = new_row
        self.game_board[old_row][old_col].col = new_col

        self.game_board[new_row][new_col] = self.game_board[old_row][old_col]
        self.game_board[old_row][old_col] = None

        self.toQueen(new_row, new_col)

        self.view.update_old_cell([old_row, old_col])
        self.view.dehighlight(buttons)
        self.view.show(self.game_board)


    def eat(self,new_cell, new_row, new_col, attacker, buttons, turn):
        nextCapture = [False,""]
        old_row = attacker[0]
        old_col = attacker[1]
        attacker = self.game_board[old_row][old_col]

        self.game_board[old_row][old_col].row = new_row
        self.game_board[old_row][old_col].col = new_col

        self.game_board[new_row][new_col] = self.game_board[old_row][old_col]
        self.game_board[old_row][old_col] = None

        self.toQueen(new_row, new_col)

        if turn == self.player:
            flag = False


            if attacker.isQueen:
                if new_row - 2 == old_row:
                    if new_col - 2 == old_col:
                        self.game_board[new_row - 1][new_col - 1] = None
                        self.view.update_old_cell([new_row - 1, new_col - 1])
                        flag = True
                    elif new_col + 2 == old_col:
                        self.game_board[new_row - 1][new_col + 1] = None
                        self.view.update_old_cell([new_row - 1, new_col + 1])
                        flag = True

            if new_col - 2 == old_col and not flag:
                self.game_board[new_row + 1][new_col - 1] = None
                self.view.update_old_cell([new_row + 1, new_col - 1])
            elif new_col + 2 == old_col and not flag:
                self.game_board[new_row + 1][new_col + 1] = None
                self.view.update_old_cell([new_row + 1, new_col + 1])
        else:
            flag = False

            if attacker.isQueen:
                if new_row + 2 == old_row:
                    if new_col - 2 == old_col:
                        self.game_board[new_row + 1][new_col - 1] = None
                        self.view.update_old_cell([new_row + 1, new_col - 1])
                        flag = True
                    elif new_col + 2 == old_col:
                        self.game_board[new_row + 1][new_col + 1] = None
                        self.view.update_old_cell([new_row + 1, new_col + 1])
                        flag = True

            if new_col - 2 == old_col and not flag:
                self.game_board[new_row - 1][new_col - 1] = None
                self.view.update_old_cell([new_row - 1, new_col - 1])
            elif new_col + 2 == old_col and not flag:
                self.game_board[new_row - 1][new_col + 1] = None
                self.view.update_old_cell([new_row - 1, new_col + 1])

        self.view.update_old_cell([old_row, old_col])
        self.view.dehighlight(buttons)

        if turn == self.player:
            if self.game_board[new_row][new_col].canEat(new_row - 1, new_col - 1, self.game_board, "player") or \
                    self.game_board[new_row][new_col].canEat(new_row - 1, new_col + 1, self.game_board, "player"):
                nextCapture = [True, new_row, new_col]

            if attacker.isQueen:
                if self.game_board[new_row][new_col].canEat(new_row + 1, new_col - 1, self.game_board, "player", True) or self.game_board[new_row][new_col].canEat(new_row + 1, new_col + 1, self.game_board, "player", True):
                    nextCapture = [True, new_row, new_col]

        if turn == self.computer:
            if self.game_board[new_row][new_col].canEat(new_row + 1, new_col - 1, self.game_board, "computer") or \
                    self.game_board[new_row][new_col].canEat(new_row + 1, new_col + 1, self.game_board, "computer"):
                nextCapture = [True, new_row, new_col]

            if attacker.isQueen:
                if self.game_board[new_row][new_col].canEat(new_row - 1, new_col - 1, self.game_board, "computer", True) or self.game_board[new_row][new_col].canEat(new_row - 1, new_col + 1, self.game_board, "computer", True):
                    nextCapture = [True, new_row, new_col]

        self.view.show(self.game_board, nextCapture)


    def computer_turn(self):
        pass

    def printBoard(self):
        for row in self.game_board:
            for piece in row:
                if piece == None:
                    print("none")
                else:
                    if piece.color == "black":
                        print("blak", piece.row, piece.col)
                    if piece.color == "white":
                        print("whit", piece.row, piece.col)
            print("-")

    def multiple_capture(self, row, col, turn):
        placings = []
        attackers = []
        piece = self.game_board[row][col]
        if turn == self.player:
            if row - 1 >= 0 and col + 1 < 8:
                if piece.canEat(row-1, col+1, self.game_board, "player"):
                    placings.append([row-2, col+2, [row, col]])
                    attackers.append([row, col])
            if row - 1 >= 0 and col - 1 >= 0:
                if piece.canEat(row-1, col-1, self.game_board, "player"):
                    placings.append([row-2, col-2, [row, col]])
                    attackers.append([row, col])

            if self.game_board[row][col].isQueen and row + 1 < 8 and col + 1 < 8:
                if piece.canEat(row+1, col+1, self.game_board, "player", True):
                    placings.append([row+2, col+2, [row, col]])
                    attackers.append([row, col])
            if self.game_board[row][col].isQueen and row + 1 < 8 and col - 1 >= 0:
                if piece.canEat(row+1, col-1, self.game_board, "player", True):
                    placings.append([row+2, col-2, [row, col]])
                    attackers.append([row, col])

            if len(placings) != 0:
                self.view.highlight_to_eat(placings, attackers)

        if turn == self.computer:
            if row + 1 < 8 and col + 1 < 8:
                if piece.canEat(row + 1, col + 1, self.game_board, "computer"):
                    placings.append([row + 2, col + 2, [row, col]])
                    attackers.append([row, col])
            if row + 1 < 8 and col - 1 >= 0:
                if piece.canEat(row + 1, col - 1, self.game_board, "computer"):
                    placings.append([row + 2, col - 2, [row, col]])
                    attackers.append([row, col])

            if self.game_board[row][col].isQueen and row - 1 >= 0 and col + 1 < 8:
                if piece.canEat(row-1, col+1, self.game_board, "computer", True):
                    placings.append([row-2, col+2, [row, col]])
                    attackers.append([row, col])
            if self.game_board[row][col].isQueen and row - 1 >= 0 and col - 1 >= 0:
                if piece.canEat(row-1, col-1, self.game_board, "computer", True):
                    placings.append([row-2, col-2, [row, col]])
                    attackers.append([row, col])

            if len(placings) != 0:
                self.view.highlight_to_eat(placings, attackers)


    def capture_options(self, turn):
        placings = []
        attackers = []
        if turn == self.player:
            for roww in self.game_board:
                for piece in roww:
                    if piece != None and piece.color == turn:
                        row = piece.row
                        col = piece.col
                        if row - 1 >= 0 and col + 1 < 8:
                            if piece.canEat(row-1, col+1, self.game_board, "player"):
                                placings.append([row-2, col+2, [row, col]])
                                attackers.append([row, col])
                        if row - 1 >= 0 and col - 1 >= 0:
                            if piece.canEat(row-1, col-1, self.game_board, "player"):
                                placings.append([row-2, col-2, [row, col]])
                                attackers.append([row, col])

                        if self.game_board[row][col].isQueen and row + 1 < 8 and col + 1 < 8:
                            if piece.canEat(row+1, col+1, self.game_board, "player", True):
                                placings.append([row+2, col+2, [row, col]])
                                attackers.append([row, col])
                        if self.game_board[row][col].isQueen and row + 1 < 8 and col - 1 >= 0:
                            if piece.canEat(row+1, col-1, self.game_board, "player", True):
                                placings.append([row+2, col-2, [row, col]])
                                attackers.append([row, col])

            if len(placings) != 0:
                self.view.highlight_to_eat(placings, attackers)

        if turn == self.computer:
            for roww in self.game_board:
                for piece in roww:
                    if piece != None and piece.color == turn:
                        row = piece.row
                        col = piece.col
                        if row + 1 < 8 and col + 1 < 8:
                            if piece.canEat(row + 1, col + 1, self.game_board, "computer"):
                                placings.append([row + 2, col + 2, [row, col]])
                                attackers.append([row, col])
                        if row + 1 < 8 and col - 1 >= 0:
                            if piece.canEat(row + 1, col - 1, self.game_board, "computer"):
                                placings.append([row + 2, col - 2, [row, col]])
                                attackers.append([row, col])

                        if self.game_board[row][col].isQueen and row - 1 >= 0 and col + 1 < 8:
                            if piece.canEat(row-1, col+1, self.game_board, "computer", True):
                                placings.append([row-2, col+2, [row, col]])
                                attackers.append([row, col])
                        if self.game_board[row][col].isQueen and row - 1 >= 0 and col - 1 >= 0:
                            if piece.canEat(row-1, col-1, self.game_board, "computer", True):
                                placings.append([row-2, col-2, [row, col]])
                                attackers.append([row, col])

            if len(placings) != 0:
                self.view.highlight_to_eat(placings, attackers)

class MyGame:
    def __init__(self):
        root = Tk()
        root.title('Checkers')
        the_game = Game_2players(root, "white", "black")
        root.mainloop()
        root.destroy()
        del root
        gc.collect()
        self.winner = the_game.winner

cands = Players.find_all("./plugs")

for cand_a in cands:
    for cand_b in cands:
        if (cand_a == cand_b):
            continue
        succ = Players.load(cand_a, cand_b)
        if (not succ):
            continue
        with suppress(Exception):
             new_game = MyGame()
             if (new_game.winner == Consts.DRAW):
                 print_winner = Consts.DRAW
             else:
                 print_winner =  Players.base2 if (new_game.winner == "white") else Players.base1
             file_object = open('sample.txt', 'a')
             file_object.write(Players.base1 + "," + Players.base2 + "," + print_winner + '\n')
             file_object.close()












