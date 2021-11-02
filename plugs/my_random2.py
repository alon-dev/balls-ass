import random
import itertools

def my_random2(game_board, color, count, timeout):
    placings = {}
    eatings = {}
    turn = "player" if (color == "white") else "computer"

    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] != None and  game_board[i][j].color == color:
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
        
    if (len(array_to_use) == 0):
            return ()

    cellS = random.randint(0, len(array_to_use)-1)
    start = list(itertools.islice(array_to_use, cellS,cellS+1))[0]
    cellT = random.randint(0, len(array_to_use[start])-1)
    target = list(itertools.islice(array_to_use[start], cellT,cellT+1))[0]
    target = tuple(target)

    return start + target
    
    