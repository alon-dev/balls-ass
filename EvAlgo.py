from copy import copy
import numpy as np
from fishkel_bot import Model
import time
# returns true if bot1 wins bot2, else its false


def algo():
    start = time.perf_counter()
    start_arr = [20,1,3,5,7,9,11,13]
    learning_val = 5
    lerning_curve = 0.8
    while True:
        weigths = []
        for i in range(8):
            copy = start_arr.copy()
            copy[i] += learning_val
            weigths.append(copy)
            copy = start_arr.copy()
            copy[i] -=learning_val
            weigths.append(copy)
        while len(weigths) > 1:
            new_weights = []
            for i in range(len(weigths)):
                try:
                    winner = check_winner(weigths[2*i], weigths[2*i +1])
                    new_weights.append(winner)
                except:
                    continue
            weigths = new_weights
        start_arr = weigths[0]
        print(start_arr)
        learning_val *= lerning_curve
    print("running time: " + str(time.perf_counter() - start))
    with open("result.txt",'w') as f:
        f.writelines(str(start_arr))
        

def check_winner(weights1, weights2):
    print(weights1, " vs ", weights2)
    bot = True
    moves = 1
    model = Model(None, weights1)
    score1 = model.score(len(model.all_possible(not bot)), 0, not bot)
    while moves < 50 and score1 < 100000 and score1 > -100000:
        if bot:
            model.weights = weights1
            move = model.minimax(3, True, None)[1]
        else:
            model.weights = weights2
            move = model.minimax(3, False, None)[1]
        if move != None:
            model.make_move(move[0], move[1])
        bot = not bot
        score1 = model.score(len(model.all_possible(not bot)), 0, not bot)
        moves += 1

    bot = True
    moves = 1
    model = Model(None, weights1)
    score2 = model.score(len(model.all_possible(not bot)), 0, not bot)
    while moves < 50 and score1 < 100000 and score1 > -100000:
        if bot:
            model.weights = weights2
            move = model.minimax(6, True, None)[1]
        else:
            model.weights = weights1
            move = model.minimax(6, False, None)[1]
        if move != None:
            model.make_move(move[0], move[1])
        bot = not bot
        score2 = model.score(len(model.all_possible(not bot)), 0, not bot)
        moves += 1

    if score1 + score2 <= 0:
        return weights1
    return weights2
print(algo())