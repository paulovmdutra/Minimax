# -*- coding: utf-8 -*-
from math import inf as infinity
from random import choice
import platform
import time
from os import system

from Board import Board
from Minimax import Minimax
from Position import Position

def main():
    
    b = Board()
    miniMax = Minimax()
    print("Start the game")
    while(b.has_winner() == Board.State.CONTINUE):
        
        position = Position(-1,-1)
        
        if (b.get_turn_to_player() is Board.State.IA):                                    
            print("\nIA PLAYING")
            position = miniMax.best_move(b, Minimax.Turn.HUMAN)            
        else:
            print("\nHUMAN PLAYING")
            position = miniMax.best_move(b, Minimax.Turn.IA)            
            #position = b.random_move()
            
        if (position != None):            
            print("Playing in position: " + str(position))
            b.set_move(position.x, position.y)
            print("Available positions: " + str(b.size_available_positions()))
            print("Total movements: " + str(b.size_moves()))
            b.print_move()
            time.sleep(1)

    print("Winner: " + str(b.get_winner()))

if __name__ == '__main__':
    main()