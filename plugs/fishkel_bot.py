from demo import *
import numpy as np
import itertools

def is_terminal(depth, board, length):
    if depth <= 0 or length == 0:
        return True
    return False
def can_eat(game_board, color, i, j):
    eatings = []
    turn = "player" if (color == "white") else "computer"
    candiate_eatings = [(i+1,j+1), (i+1,j-1), (i-1,j+1), (i-1,j-1)]
                    # eating has mandatory priority
    for eat in candiate_eatings:
        if game_board[i][j].canEat(eat[0], eat[1], game_board, turn, game_board[i][j].isQueen):
            eatings.append((eat[0]-i+eat[0], eat[1]-j+eat[1]))
                    # if no eating lets check regular move
    
    return len(eatings) != 0

def make_move(board, move):
    start = move[0][0]
    end = move[0][1]
    middle = ((start[0] + end[0])//2, (start[1] + end[1])//2)
    is_eat = move[1]

    if is_eat:
        board[middle[0]][middle[1]] = None
    
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = None

def reverse_move(board, move):
    start = move[0][0]
    end = move[0][1]
    temp = board[start[0]][start[1]]
    board[start[0]][start[1]] = board[end[0]][end[1]]
    board[end[0]][end[1]] = temp
def give_score(board, length, maximizingPlayer, weights_arr):
    if length == 0:
        if maximizingPlayer:
            return float('inf')
        return float('-inf')
    weights_arr = weights_arr
    white_pieces = []
    black_pieces = []
    for i in range (len(board)):
        for j in range(len(board)):
            if board[i][j]:
                if board[i][j].color == "white":
                    white_pieces.append(board[i][j])
                else:
                    black_pieces.append(board[i][j])
            else:
                continue
    score = 0.0
    white_queens = []
    black_queens = []
    white_attacking = []
    white_defending = []
    black_attacking = []
    black_defending = []
    for piece in white_pieces:
        if piece.row > 4:
            white_attacking.append(piece)
        else:
            white_defending.append(piece)
        if piece.isQueen:
            white_queens.append(piece)
    for piece in black_pieces:
        if piece.row > 4:
            black_attacking.append(piece)
        else:
            black_defending.append(piece)
        if piece.isQueen:
            black_queens.append(piece)
    score += weights_arr[0] * len(white_queens)
    score += weights_arr[1] * len(white_defending)
    score += weights_arr[2] * len(white_attacking)
    
    score -= weights_arr[0] * len(black_pieces)
    score -= weights_arr[1] * len(black_defending)
    score -= weights_arr[2] * len(black_attacking)
    
    score = score


    return score
def minimax(board, depth, maximizingPlayer, hungry_piece, weights_arr):
    same_turn = None
    best_move = None
    color = "white"
    if maximizingPlayer is False:
        color = "black"
    
    possible_moves = all_options(board, color)
    if hungry_piece is not None:
        possible_eatings_with_piece = [move for move in possible_moves if move[0][0] == hungry_piece]
        if len(possible_eatings_with_piece) > 0:
            possible_moves = possible_eatings_with_piece
    
    if is_terminal(depth, board, len(possible_moves)):
        return (give_score(board, len(possible_moves), maximizingPlayer, weights_arr), None)
    if maximizingPlayer:
        max_score = float('-inf')
        for move in possible_moves:
            make_move(board, move)
            if move[1] == 0:
                score = minimax(board, depth-1, maximizingPlayer, move[0][1], weights_arr)[0]
            else:
                score = minimax(board, depth-1, not maximizingPlayer, None, weights_arr)[0]
            #if hungry_piece is none, then the last move was not an eating.
            reverse_move(board, move)
            if score > max_score:
                max_score = score
                best_move = tuple(move[0][0]) + tuple(move[0][1])        
        return (max_score, best_move)
    else:
        min_score = float('inf')
        for move in possible_moves:
            make_move(board, move)
            if move[1] == 0:
                score = minimax(board, depth-1, maximizingPlayer, move[0][1], weights_arr)[0]
            else:
                score = minimax(board, depth-1, not maximizingPlayer, None, weights_arr)[0]
            #if hungry_piece is none, then the last move was not an eating.
            reverse_move(board, move)
            if score < min_score:
                min_score = score
                best_move = tuple(move[0][0]) + tuple(move[0][1])
        return (min_score, best_move)


def all_options(game_board, color):
    placings = {}
    eatings = {}
    turn = "player" if (color == "white") else "computer"

    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] != None and game_board[i][j].color == color:
                candiate_eatings = [(i+1,j+1), (i+1,j-1), (i-1,j+1), (i-1,j-1)]
                # eating has mandatory priority
                for eat in candiate_eatings:
                    if game_board[i][j].canEat(eat[0], eat[1], game_board, turn, game_board[i][j].isQueen):
                        if ((i,j) not in eatings):
                                eatings[(i,j)] = []
                        eatings[(i,j)].append((eat[0]-i+eat[0], eat[1]-j+eat[1]))
                # if no eating lets check regular move
                if (len(eatings) == 0):
                    options = game_board[i][j].possible_placing(game_board)
                    if (len(options) > 0):
                        for k in range(len(options)):
                            placings[(i,j)]  = options

    if (len(eatings) > 0):
        array_to_use = (eatings, 0)
    else:
        array_to_use = (placings, 1)

    all_options = []
    for option in array_to_use[0]:
        for possible_move in array_to_use[0][option]:
            all_options.append(((option, possible_move),array_to_use[1]))
    return all_options




def fishkel_bot(game_board, color, count, timeout, hungry_piece, weights_arr=[10,5,7]):
    print("fishkel gay: " + color)
    if color == "white":
        return minimax(game_board, 6, True, hungry_piece,weights_arr)[1]
    else:
        return minimax(game_board, 6, False, hungry_piece,weights_arr)[1]


