#lets see how many simulations we can complete 
import sys
import time
import random
from typing import Callable
import concurrent.futures
import multiprocess
import numpy as np
from checkers import checkers as checkers_game

def simulate(startPlayer:int=1, allowBackjump:bool=False, requireJump=True, maxMoves = 200)->int:
    '''
        Returns the Winner
    '''
    game = checkers_game()
    player = startPlayer
    m = maxMoves

    moves_1 = []
    moves_2 = []

    while m >= 0:
        moves = []
        jumps = []
        pieces = list(zip(*np.where(game.board&3&player == player)))
        
        for p in pieces:
            moves.extend(list(game._moves(p)))
            #jumps.extend(list(game._jumps(p,allowBackJump=allowBackjump)))
            # if not requireJump:
            #     moves.extend(jumps)
        if len(moves) == 0: break

        rm:checkers_game.Movement = None

        if requireJump and len(jumps) > 0:
            rm = random.choice(jumps) 
        else:
            rm = random.choice(moves)
        
        rm = game.move(rm)
        if player == 1: moves_1.append(rm)
        if player == 2: moves_2.append(rm)

        while rm.subsequent != None and len(rm.subsequent) > 0:
            rm = random.choice(rm.subsequent)
            game.move(rm)
            if player == 1: moves_1.append(rm)
            if player == 2: moves_2.append(rm)


        player = 3^(player&3)
        m -= 1
        
    return 0 if moves==0 else 3^(player&3),moves_1, moves_2

def __runsim(i):
    s = time.time()
    winner, moves1, moves2 = simulate()
    e = time.time()        
    # if callback : callback(i, (e-s),winner,moves1,moves2)
    return (i,winner,moves1,moves2)

def runSimulations(count:int=1, callback:Callable[[int,int,list,list],None] = None):

    start = time.time()
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #    executor.map(__runsim,range(count))
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     results = executor.map(__runsim,range(count))

    for i in range(count):
        s = time.time()
        winner, moves1, moves2 = simulate()
        e = time.time()        
        if callback : callback(i, (e-s),winner,moves1,moves2)

    end = time.time()
    #return (end-start), winners

if __name__ == "__main__":
    start =time.time()
    sys.setrecursionlimit(10**9)
    runSimulations(1000)
    end = time.time()
    print(end-start)