#game
from collections import namedtuple
from dataclasses import dataclass
from io import StringIO
from typing import NamedTuple
import numpy as np


class checkers:
    def __init__(self, height=8, width =8):
        self.board = np.zeros((8,8),dtype=np.int8)
        self.height = height
        self.width = width
        self.board[0:3:2, 1:8:2] = 1
        self.board[1, 0:8:2] = 1
        self.board[6:8:2, 1:8:2] = 2
        self.board[5:8:2, 0:8:2] = 2
        self.winner = 0

    @dataclass
    class Movement:
        start:NamedTuple("start",[('row',int), ('col',int)])
        end:NamedTuple("end",[('row',int), ('col',int)])
        jump:NamedTuple("jump",[('row',int), ('col',int)]) = None
        subsequent: list = None
        
        def __toChar(self,position):
            if position == None: return ""
            retval = chr(ord('`')+position[0]+1), str(position[1])
            return retval

        def __str__(self):
            val = ''.join(self.__toChar(self.start)) +'->'+''.join(self.__toChar(self.end))+('∩'+''.join(self.__toChar(self.jump)) if self.jump else '')
            return val
        
        def __repr__(self):
            return self.__str__()
        
    def _posToStr(self,position):
        if position == None: return ""
        return chr(ord('`')+position[0]+1) + str(position[1])
    
    def _strToPos(self,position):
        if position == None: return ""
        return int(ord(position[0])-ord('a')), int(position[1])

    def __valid(self,position):
        if position == None: return False
        r,c = position
        return r >= 0 and r < self.height and c >= 0 and c < self.width

    def _jumps(self,position, player = None, allowBackJump = True, exclude_from = (-1,-1)):
        if type(position) == type('str'): position = self._strToPos(position)
        jumps = []
    
        r,c = position
        if (player:= (player or self.board[position])) == 0:  return []
        opponent = 3^(player&3)
        if player&4 == 4: allowBackJump = True
        directions = []
        if player   & 4 == 4:  directions =  [(1,1),(2,2)], [(1,-1),(2,-2)], [(-1,1),(-2,2)], [(-1,-1),(-2,-2)]
        elif player & 1 == 1:  directions =  [(1,1),(2,2)], [(1,-1),(2,-2)]
        elif player & 2 == 2:  directions =  [(-1,1),(-2,2)], [(-1,-1),(-2,-2)] 
        else: return jumps
        
        for neighbor,drop in directions:
            n = (r+neighbor[0],c+neighbor[1])
            d = (r+drop[0],c+drop[1])
            if n == exclude_from or d==exclude_from: continue
            if(not self.__valid(n) or not self.__valid(d)): continue

            if (self.board[n]&3)==opponent and self.board[d] == 0:
                jump_move = self.Movement(position,d,n) 
                jumps.append(jump_move)
                p = (player&3|4) if allowBackJump else player
                multi_jumps = self._jumps(d, player = p, allowBackJump=allowBackJump, exclude_from = position)
                jump_move.subsequent = multi_jumps
        return jumps
         
    def _moves(self,position) -> list:
        if type(position) == type('str'): position = self._strToPos(position)
        row, col = position
        if (player:= self.board[position]) == 0:  return []
        directions = []
        if   player&4==4: directions = [(1,-1),(1,1),(-1,-1),(-1,1)] 
        elif player&2==2: directions = [(-1,-1),(-1,1)]
        elif player&1==1: directions = [(1,-1),(1,1)]

        for dr,dc in directions:
           if self.__valid((row+dr,col+dc)) and self.board[row+dr,col+dc] == 0: yield self.Movement(position,(row+dr,col+dc))
        
    def move(self,move:Movement):
        x1,y1 = move.start
        x2,y2 = move.end
        jx,jy = -1,-1 or move.jump
        if(move.jump): 
            self.jump(move)
            p = self.board[x2,y2]
        else:
            p = self.board[x1,y1]
            self.board[x1,y1] = 0
            self.board[x2,y2] = p

        if p&3 == 1 and x2 == self.height-1: self.board[x2,y2] = 5
        if p&3 == 2 and x2 == 0: self.board[x2,y2] = 6
        return move
    
    def jump(self,move:Movement):
        x1,y1 = move.start
        x2,y2 = move.end
        jx,jy = move.jump
        p = self.board[x1,y1]
        self.board[x1,y1] = 0
        self.board[x2,y2] = p
        self.board[jx,jy] = 0
        return move

    def __str__(self):
        # https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
        bold =  '\033[1m'
        borderColor = bold+'\033[90m'
        brightBorderColor = bold+'\033[37m'
        end_color = '\033[0m'
        underline = '\033[4m'
        red = bold+'\033[91m'
        green = bold+'\033[92m'
        out = StringIO()
        print('    ' + underline,end="",file=out)
        for i in range(self.board.shape[1]):
            print(f"   {i}  ",end="",file=out)
        print(' '+ end_color,file=out)
        for row in range(self.board.shape[0]):
            print("|",end="",file=out)
            print(" "*3,end="",file=out)
            print(f"{borderColor}+-----"*8, end=f"+\n",file=out)
            print(end_color + f"|{  chr(ord('`')+row+1)  }  "+ borderColor,end="",file=out)
            for col in range(self.board.shape[1]):
                color = red if self.board[row,col]&3&1 == 1 else green if self.board[row,col]&3&2 == 2 else borderColor
                char = 'K' if self.board[row,col] & 4 == 4 else '@' if self.board[row,col] != 0 else ' '
                print(f"| {color} {char}  {borderColor}",end="",file=out)
            print(f"|{end_color}",file=out)
                
        print("|",end="",file=out)
        print(" "*3,end="",file=out)
        print(f"{borderColor}+-----"*8, end=f"+{end_color}\n",file=out)
        return out.getvalue()
    
    def __repr__(self) -> str:
        return self.__str__()  
