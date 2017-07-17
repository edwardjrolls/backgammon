import board
import sys
import numpy as np


# The storage class, which is used to store the collection of board states
class GammonAIbase:
    # Initialise the storage
    def __init__(self):
        self.gameCollection = {'w':[],'l':[]} # This is a dictionary, where the key is whether the home player wins or loses, and the value is the board positions associated
    
    # Empty the storage
    def emptyStorage(self):
        self.gameCollection = {'w':[],'l':[]}
    
    # Play a game and add it to the storage
    def playGame(self,strategyA='random',strategyB='random',parametersA=None,parametersB=None):
        gameBoard = board.Board(strategyA,strategyB,parametersA,parametersB)
        winner,history = gameBoard.game()
        if winner==1:
            self.gameCollection['w']+=history[1]
            self.gameCollection['l']+=history[2]
        else:
            self.gameCollection['w']+=history[2]
            self.gameCollection['l']+=history[1]
    
    # Play n games
    def trainModel(self,n,strategyA='random',strategyB='random',parametersA=None,parametersB=None):
        for _ in range(n):
            self.playGame(strategyA,strategyB,parametersA,parametersB)
    
    # Play n games between two strategies
    def compareModels(self,n,strategyA='random',strategyB='random',parametersA=None,parametersB=None):
        winsA=0
        winsB=0
        for _ in range(n):
            gameBoard = board.Board(strategyA,strategyB,parametersA,parametersB)
            winner,_ = gameBoard.game()
            if winner==1:
                winsA+=1
            else:
                winsB+=1
        print("Strategy A has " + str(winsA) + " wins, compared to " + str(winsB) + " for strategy B.")
        
            
if __name__=='__main__':
    e = GammonAIbase()
    for i in range(10):
        e.playGame()
        print(i)



