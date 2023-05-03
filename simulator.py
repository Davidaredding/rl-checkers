import os
import random

import numpy as np
import checkers as g
from time import sleep
   
game = g.checkers()


while True:
    redMoves = []
    redPlayers = list(zip(*np.where(game.board&3&1 == 1)))
    for p in redPlayers:
        redMoves.extend(list(game._moves(p)))
        redMoves.extend(list(game._jumps(p,allowBackJump=False)))
    if(len(redMoves) == 0): break

    os.system('cls' if os.name=='nt' else 'clear')
    print('red')
    rm = random.choice(redMoves)
    print(list(map(str,redMoves)))
    game.move(rm)
    print(rm)
    while rm.subsequent != None and len(rm.subsequent) > 0:
        rm = random.choice(rm.subsequent)
        game.move(rm)
   
    print(game)
    sleep(.75)
    greenMoves = []
    greenJumps = []

    greenPlayers = list(zip(*np.where(game.board&3&2 == 2)))
    for p in greenPlayers:
        greenMoves.extend(list(game._moves(p)))
        greenJumps.extend(list(game._jumps(p,allowBackJump=False)))

    if(len(greenMoves) == 0 and len(greenJumps)==0): 
        print(list(game._moves((5,0))))
        break

    os.system('cls' if os.name=='nt' else 'clear')
    print('green')
    print(list(map(str,greenMoves)))
    
    if len(greenJumps) > 0:
        gm = random.choice(greenJumps)
    else:
        gm = random.choice(greenMoves)
 
    game.move(gm)
    print(gm)
    while gm.subsequent != None and len(gm.subsequent) > 0:
        gm = random.choice(gm.subsequent)
        game.move(gm)
        print(gm)
    print(game)
    sleep(.75)
