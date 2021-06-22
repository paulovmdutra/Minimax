import time
import copy
from enum import Enum

from Position import Position 
from Board import Board

#Minimax class
class Minimax:
    
    MAX_INT  = 2147483648
    MIN_INT  = -2147483648
    
    debug = False
    check_move_opponent = True
    
    class Turn(Enum):
        IA = True,
        HUMAN = False

    #IA to found out the winning strategy 
    def minimax(self, board, depth, turn, alpha, beta):
        
        bestScore = 0
        state = self.evaluate(board)
	
        if ( (state != Board.State.CONTINUE) or (depth == 0) ):		
            
            if (self.debug):
                print("State: " + str(state) + " - Depth: " + str(depth))
            
            if (self.debug):
                board.print_move()
                print("\n")
                #time.sleep(1)
                
            return state.value[0]
        
        if (turn == self.Turn.IA):
            bestScore = self.maximize(board, depth, alpha, beta)
        else:
            if (turn == self.Turn.HUMAN):
                bestScore = self.minimize(board, depth, alpha, beta)        
        
        return bestScore

    # Maximize
    def maximize(self, board, depth, alpha, beta):	
        
        bestScore = self.MIN_INT        

        for x in range(board.width):   
            for y in range(board.height):       
                pos = Position(x, y) 
                
                if (self.debug):
                    print("Maximize(Testando movimento: X: " + str(pos.x) + " Y: " + str(pos.y) + ")")                    
                    
                if (board.is_empty_position(pos.x, pos.y)):                                    
                    if (self.debug):
                        print("\n")
                        
                    board.set_move(pos.x, pos.y)				
                    score = self.minimax(board, depth-1, self.Turn.HUMAN, alpha, beta)
                    board.undo_move()				                
                    bestScore = max(score, bestScore)
                
                #alpha = max(alpha, score);
                
                #if (beta <= alpha):
                #   break;
                 
        if (self.debug):
            print("Score Maximize: " + str(bestScore))	
        return bestScore

    # Minimize	
    def minimize(self, board, depth, alpha, beta):
        
        bestScore = self.MAX_INT
                
        for x in range(board.width):   
            for y in range(board.height):       
                pos = Position(x, y) 
                if (board.is_empty_position(pos.x, pos.y)):
                    board.set_move(pos.x, pos.y)				
                    score = self.minimax(board, depth-1, self.Turn.IA, alpha, beta)
                    board.undo_move()		                
                    bestScore = min(score, bestScore)	
                    
                    #beta = min(beta, score);                    
                                
                    #if (beta <= alpha):
                     #   break;                
                 
        if (self.debug):
            print("Score Minimize: " + str(bestScore))			
            
        return bestScore

    #Checks the best movement for I.A
    def best_move(self, board, turn):
        
        position = Position(-1,-1)
        bestScore = self.MIN_INT
        
        if (self.debug):
            print("CHECKING THE BETTER MOVEMENT")                
        
        winner = False;        
        finalizou = False
        
        for x in range(board.width):   
            for y in range(board.height):       
                pos = Position(x, y) 
                if (board.is_empty_position(pos.x, pos.y)):
                    
                    if (self.debug):    
                        print("EMPTY POSITION: " + str(board.is_empty_position(pos.x, pos.y)))
                        print("Best Move(Testando movimento: X: " + str(pos)) 
                    
                    board.set_move(pos.x, pos.y)
                    
                    score = self.minimax(board, 100, turn, self.MIN_INT, self.MAX_INT)
                    
                    #Here, I check if there is a winner, this way, 
                    #isn't necessary to check all positions if there is a winner.
                    if (board.check_winner() == Board.State.IA and turn == self.Turn.HUMAN):
                        position = pos
                        winner = True                        
                        if (self.debug):    
                            print("FOUND OUT THE BEST MOVEMENT: IA GO WINNER: ")
                            time.sleep(3)
                        finalizou = True                        
                    else:
                        if (board.check_winner() == Board.State.HUMAN and turn == self.Turn.IA):
                            position = pos
                            winner = True                            
                            if (self.debug):    
                                print("FOUND OUT THE BEST MOVEMENT: HUMAN GO WINNER: ")
                                time.sleep(3)
                            finalizou = True                            

                    board.undo_move()
                    
                    if (winner):                        
                        break
                    
                    if (score > bestScore):
                        position = pos
                        bestScore = score    
                        if (self.debug):
                            print("ONLY FOUND OUT THE BEST MOVEMENT: " + str(position))
                            time.sleep(3)
                            
            if (finalizou):
                break

        #Verifica se o adversário podera ganhar na próxima jogada, caso seja verdadeira,
        #bloquea a jogada
        if (self.check_move_opponent) and not winner:
            p = self.checks_opponent_winner(board, turn)
            if (p != None):
                position = p
        
        if (self.debug):        
            print("THE BETTER MOVEMENT: " + position.to_string() )
            
        return position

    #Heuristic evaluation of state
    def evaluate(self,board):
        state = board.has_winner()
        return state
    
    #Checks if the opponent winner
    def checks_opponent_winner(self,board,turn):
        
        if (self.debug):
            print("CHECKING THE MOVEMENT OF OPPONENT")            
                    
        boardCopy = copy.deepcopy(board)
        #boardCopy.set_board(board)
        positionOpponent = None
        winner = False
        
        for x in range(boardCopy.width):   
            for y in range(boardCopy.height):       
                
                pos = Position(x, y)
                if (boardCopy.is_empty_position(pos.x, pos.y)):                        
                    
                    if (turn == self.Turn.HUMAN):                              
                        
                        boardCopy.board[pos.x][pos.y] = Board.Mark.O                            
                        if (self.debug):
                            print("VERIFICANDO SE O HUMANO GANHA: " + str(boardCopy.check_winner()))
                            
                        if (boardCopy.check_winner() == Board.State.HUMAN):
                            winner = True
                            positionOpponent = pos                                
                            if (self.debug):
                                print("HUMANO GANHARA")
                            
                    else:
                        if (turn == self.Turn.IA):                                
                            
                            boardCopy.board[pos.x][pos.y] = Board.Mark.X
                            if (self.debug):
                                print("VERIFICANDO SE O IA GANHA: " + str(boardCopy.check_winner()))
                                
                            if (boardCopy.check_winner() == Board.State.IA):
                                winner = True
                                positionOpponent = pos
                                if (self.debug):
                                    print("IA GANHARA")                                        
                                
                    boardCopy.board[pos.x][pos.y] = Board.Mark.EMPTY                        
                    if (winner):
                        break                        
                    
                #endif
                
            #end for
            
            if (winner):
                break                
            
        #end for
        
        if (self.debug):
            print("MOVEMENT THE OPONENT CHECKED: " + str(positionOpponent))
            time.sleep(2)
        
        position = None
        
        if (positionOpponent != None) and winner:
            position = positionOpponent
            if (self.debug):
                if (turn == self.Turn.HUMAN):              
                    print("HUMAN WINNER, SO, I WILL PLAY HERE: " + str(positionOpponent))
                else:
                    if (turn == self.Turn.IA):                  
                        print("IA WINNER, SO, I WILL PLAY HERE: " + str(positionOpponent))
                
                time.sleep(2)
        
        return position        