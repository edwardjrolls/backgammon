import board
import sys


# The storage class, which is used to store the collection of board states
class GameStorage:
    # Initialise the storage
    def __init__(self,strategyA='random',strategyB='random'):
        self.gameCollection = {'w':[],'l':[]} # This is a dictionary, where the key is whether the home player wins or loses, and the value is the board positions associated
        self.strategyA = strategyA
        self.strategyB = strategyB
    
    # Play a game and add it to the storage
    def playGame(self):
        gameBoard = board.Board(self.strategyA,self.strategyB)
        winner,history = gameBoard.game()
        if winner==1:
            self.gameCollection['w']+=history[1]
            self.gameCollection['l']+=history[2]
        else:
            self.gameCollection['w']+=history[2]
            self.gameCollection['l']+=history[1]
        
            

e = GameStorage()
for i in range(1000):
    e.playGame()
    print(i)

