from copy import copy
import numpy as np

# returns true if bot1 wins bot2, else its false
def check_winner(bot1, bot2):
    pass



def algo():
    best_arr = [10,5,7]
    learning_val = 5
    lerning_curve = 0.8
    while learning_val > 0.05:
        weigths = [best_arr.copy()]
        for i in range(3):
            copy = best_arr.copy()
            copy[i] += learning_val
            weigths.append(copy)
            copy = best_arr.copy()
            copy[i] -=learning_val
            weigths.append(copy)
        for i in weigths:
            if check_winner(weigths,best_arr):
                best_arr = weigths
        learning_val *= lerning_curve
    return best_arr

