from demo import *
import itertools

def is_terminal(depth, board, length):
    if depth <= 0 or length == 0:
        return True
    return False
    
def score(board, length, maximizingPlayer):
    if length == 0:
        if maximizingPlayer:
            return float('inf')
        return float('-inf')
    weights_arr = [10, 5, 7]
    white_pieces = []
    black_pieces = []
    for i in range (len(board)):
        for j in range(len(board)):
            if board[i][j].color == "white":
                white_pieces.append(board[i][j])
            else:
                black_pieces.append(board[i][j])
    score = 0
    white_queens = []
    black_queens = []
    white_attacking = []
    white_defending = []
    black_attacking = []
    black_defending = []
    for piece in white_pieces:
        if piece.i > 4:
            white_attacking.append(piece)
        else:
            white_defending.append(piece)
        if piece.isQueen:
            white_queens.append(piece)
    for piece in black_pieces:
        if piece.i > 4:
            black_attacking.append(piece)
        else:
            black_defending.append(piece)
        if piece.isQueen:
            black_queens.append(piece)
    score += weights_arr[0] * white_queens
    score += weights_arr[1] * white_defending
    score += weights_arr[2] * white_attacking
    score -= weights_arr[0] * black_pieces
    score -= weights_arr[1] * black_defending
    score -= weights_arr[2] * black_attacking
    return score

def minimax(board, depth, maximizingPlayer):
    best_move = None
    color = "white"
    if maximizingPlayer == False:
        color = "black"
    possible_moves = all_options(board, color)
    if is_terminal(depth, board, len(possible_moves)):
        return score(board, len(possible_moves), maximizingPlayer)
    if maximizingPlayer:
        max_score = float('-inf')
        for move in possible_moves:
            new_board = make_move(board, move)
            score = minimax(new_board, depth-1, False)[0]
            if score > max_score:
                max_score = score
                best_move = move
        
        return (max_score, best_move)
    else:
        min_score = float('inf')
        for move in possible_moves:
            new_board = make_move(board, move)
            score = minimax(new_board, depth-1, True)[0]
            if score < min_score:
                min_score = score
                best_move = move
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
        array_to_use = eatings
    else:
        array_to_use = placings

    all_options = []
    for option in array_to_use:
        for possible_move in array_to_use[option]:
            all_options.append((option, possible_move))
    return all_options






def fishkel_bot(game_board, color, count, timeout):
    if color == "white":
        return minimax(game_board, 5, True)[1]
    else:
        return minimax(game_board, 5, False)[1]
    



