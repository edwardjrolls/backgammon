import copy
import random
from sys import stdin
"""
Note that a gamestate is given by a length 26 vector:
0 - 23: Each point on the board, with +ve values for home player (i.e. the next move)'s pieces, -ve for oppo
24: Hit pieces of player (+ve values)
25: Hit pieces of oppo (-ve values)
"""

"""
2 KNOWN BUG:
1)  To end the game, if we have a piece at 1 and a rolle of (6,1), then the correct move is [(1,0),(0,-6)].
    Only need a minor tweak & shouldn't make a difference to who wins
2)  Printing doesn't want to show 'X' just 'O' in the dead zone
"""

# The board class, which doesn't require any inputs
class Board:
    
    # Initialise the board
    def __init__(self,gamestate=None,strategyA='random',strategyB='random'):
        # If no gamestate given, then initialise the board
        if not gamestate:
            gamestate = self.newBoard()
        self.gamestate = gamestate
        self.strategyA=strategyA
        self.strategyB=strategyB
         
    
    # Allows a board to be printed. X for away player, O for home player
    def __str__(self):
        string = '-'*42+'\n'
        string += '|' + ' '*40 + '|\n'
        # Number the board
        string+= '|  '
        for i in range(12,24):
            string+=str(i).zfill(2)+' '
        string+='  |\n'
        # First row of upper board
        string+= '|   '
        for i in range(12,24):
            if abs(self.gamestate[i])>5:
                string+=str(abs(self.gamestate[i]))
            elif self.gamestate[i]>0:
                string+='O'
            elif self.gamestate[i]<0:
                string+='X'
            else:
                string+='|'
            string+='  '
        string+=' |\n'
        # Next 4 rows of upper board
        for j in range(1,5):
            string+='|   '
            for i in range(12,24):
                if self.gamestate[i]>j:
                    string+='O'
                elif self.gamestate[i]<-j:
                    string+='X'
                else:
                    string+='|'
                string+='  '
            string+=' |\n'
        #empty row
        string += '|' + ' '*40 + '|\n'
        # How many dead tokens
        string += '|' + ' '*3 + 'X'*self.gamestate[25] + ' '*(15-self.gamestate[25]) + ' '*4
        string += ' '*(15-self.gamestate[24]) + 'O'*self.gamestate[24] +' '*3 + '|\n'
        #empty row
        string += '|' + ' '*40 + '|\n'
        # Top 4 rows of lower board
        for j in range(4,0,-1):
            string+='|   '
            for i in range(11,-1,-1):
                if self.gamestate[i]>j:
                    string+='O'
                elif self.gamestate[i]<-j:
                    string+='X'
                else:
                    string+='|'
                string+='  '
            string+=' |\n'
        # Final row of lower board
        string += '|   '
        for i in range(11,-1,-1):
            if abs(self.gamestate[i])>5:
                string+=str(abs(self.gamestate[i]))
            elif self.gamestate[i]>0:
                string+='O'
            elif self.gamestate[i]<0:
                string+='X'
            else:
                string+='|'
            string+='  '
        string+=' |\n'
        # Number the board
        string+= '|  '
        for i in range(11,-1,-1):
            string+=str(i).zfill(2)+' '
        string+='  |\n'
        string += '|' + ' '*40 + '|\n'
        string += '-'*42
        return string
                
    
    # Sets up a new board with standard piece placings
    def newBoard(self):
        gamestate = [0]*26
        gamestate[0] = -2
        gamestate[5] = 5
        gamestate[7] = 3
        gamestate[11] = -5
        gamestate[12] = 5
        gamestate[16] = -3
        gamestate[18] = -5
        gamestate[23] = 2
        return gamestate
    
    # Gives the new 'state' following a move of the form (start,finish)
    def changeState(self,state,move):
        if move[1]<0:
            state[move[0]]-=1
        elif state[move[0]]<1:
            raise ValueError("No tiles exist at this space")
        elif state[move[1]]<-1:
            raise ValueError("Move onto a blocked tile")
        elif state[move[1]]==-1:
            state[move[1]]=1
            state[25]-=1
            state[move[0]]-=1
        else:
            state[move[1]]+=1
            state[move[0]]-=1
        
    # Find a list of legal moves for dice roll where the two dice are not equal, done in the order die1 then die2
    def potentialMovesOrder(self,die1,die2):
        firstMoveList = []
        finalMoveList = []
        state = copy.copy(self.gamestate)
        # Make the first move
        maxPiece = max([i for i in range(25) if state[i]>0])
        if state[24]>0:
            pieceStart = [24]
        else:
            pieceStart = [i for i in range(24) if state[i]>0]
        for i in pieceStart:
            stateCp = copy.copy(state)
            move = (i,i-die1)
            if (i+1>die1 and state[i-die1]>=-1) or (maxPiece==i and i+1<=die1) or (maxPiece<=5 and i+1==die1):
                self.changeState(stateCp,move)
                firstMoveList.append((move,stateCp))
        # Make the second move
        for firstMove,state in firstMoveList:
            try:
                maxPiece = max([i for i in range(25) if state[i]>0])
            except ValueError:
                finalMoveList = [[firstMove]]
                break
            if state[24]>0:
                pieceStart = [24]
            else:
                pieceStart = [i for i in range(24) if state[i]>0]
            for i in pieceStart:
                move = (i,i-die2)
                if (i+1>die2 and state[i-die2]>=-1) or (maxPiece==i and i+1<=die2) or (maxPiece<=5 and i+1==die2):
                    finalMoveList.append([firstMove,move])
        if not len(firstMoveList):
            return [[]]
        elif not len(finalMoveList):
            return [[mv[0]] for mv in firstMoveList]
        else:
            return finalMoveList
            
    # Find a list of legal moves for a repeated dice roll
    def potentialMovesRepeatedDice(self,die1):
        movesDict={}
        movesDict[()] = copy.copy(self.gamestate) # A move here is ((x,y),(a,b),(b,c))
        movesList=[[]]
        completeMove = []
        while len(movesList)>0:
            moves = movesList.pop()
            state = copy.copy(movesDict[tuple(moves)])
            minMoveMade = min([mv[0] for mv in moves]+[24])# Consider moves only less than the 
            #print(moves,movesList,minMoveMade,completeMove)
            if state[24]>0: # If we have any hit pieces, get them on the board
                move = (24,24-die1)
                if state[24-die1]>=-1:
                    self.changeState(state,move)
                    moves.append(move)
                    if len(moves)<4:
                        movesList.append(moves)
                    else:
                        completeMove.append(moves)
                    movesDict[tuple(moves)] = state
                else:
                    completeMove.append(moves)
            else:
                pieceStart=[i for i in range(minMoveMade+1) if state[i]>0]
                try:
                    maxPiece = max([i for i in range(25) if state[i]>0])
                except ValueError:
                    completeMove = [moves]
                    break
                moveMade = False
                for i in pieceStart:
                    movesCp = copy.copy(moves)
                    stateCp = copy.copy(state)
                    move = (i,i-die1)
                    if (i+1>die1 and state[i-die1]>=-1) or (maxPiece==i and i+1<=die1) or (maxPiece<=5 and i+1==die1):
                        self.changeState(stateCp,move)
                        movesCp.append(move)
                        if len(movesCp)<4:
                            movesList.append(movesCp)
                        else:
                            completeMove.append(movesCp)
                        moveMade=True
                        movesDict[tuple(movesCp)] = stateCp
                if not moveMade:
                    completeMove.append(moves)
        return completeMove
    
    # Returns a list of legal moves
    def legalMoveList(self,die1,die2):
        # Find the places of where pieces start
        if die1==die2:
            moveList = self.potentialMovesRepeatedDice(die1)
        else:
            moveList = self.potentialMovesOrder(die1,die2)
            moveList += self.potentialMovesOrder(die2,die1)
            """
            for move in moveList:
                move.sort(key = lambda x: 100*x[0]+x[1], reverse=True) # Order by first tile picked, then second tile
            # Need to remove copies (still some cases where the endstate is the same)
            newMoveList=[]
            moveSet=set()
            for move in moveList:
                if tuple(move) not in moveSet:
                    newMoveList.append(move)
                    moveSet.add(tuple(move))
            moveList = newMoveList
            """
        maxMovesMade = max([len(moves) for moves in moveList])
        moveList = [moves for moves in moveList if len(moves)==maxMovesMade]
        return(moveList)
    
    
    # Flips the board (call after a move to signify it is the opposition's move
    def flipBoard(self):
        self.gamestate = [-self.gamestate[i] for i in range(23,-1,-1)]+[-self.gamestate[25]]+[-self.gamestate[24]]

    # Make a random move
    def randomMove(self,die1,die2):
        moveList = self.legalMoveList(die1,die2)
        if len(moveList)>0:
            return random.choice(moveList)
        else:
            return tuple()
        
    # Import a player move from the input line
    def inputPlayerMove(self):
        moveMade=False
        while not moveMade:
            try:
                move = tuple(map(int,stdin.readline().rstrip().split(',')))
                moveMade=True
            except ValueError:
                print("Not recognised as a valid input. Please retry")
        return move
            
    
    
    # Allow the player to choose the move
    def playerMove(self,die1,die2):
        print(self)
        moveList = self.legalMoveList(die1,die2)
        legalMove = False
        while not legalMove:
            print("The roll is {} and {}".format(die1,die2))
            print("Move format is a,b to move from a to b. Deadzone is 24.")
            print("If no moves are possible just return (-1,-1). Please pick moves in order they would be made")
            moves=[]
            print("What is move 1?")
            moves.append(self.inputPlayerMove())
            print("What is move 2?")
            moves.append(self.inputPlayerMove())
            if die1 == die2:
                print("What is move 3?")
                moves.append(self.inputPlayerMove())
                print("What is move 4?")
                moves.append(self.inputPlayerMove())
                moves.sort(key=lambda x: x[0],reverse=True) # So that this is compatable with how moves are generated for the legal move list
            # Remove any non-moves
            while (-1,-1) in moves:
                moves.remove((-1,-1))
            if moves in moveList:
                legalMove=True
            else:
                print("\nMove is not legal. Please re-enter\n")
        return moves

    # Chooses a move in the game, sending to other functions depending on what the strategy is
    def chooseMove(self,strategy,die1,die2):
        if strategy=='random':
            move = self.randomMove(die1,die2)
        if strategy=='human':
            move = self.playerMove(die1,die2)
        return move
        
    # Make a move
    def makeMove(self,moves):
        for move in moves:
            self.changeState(self.gamestate,move)

    # A turn in the game. Ask player A for a move, flip the board, ask player B for a move, flip the board
    def turn(self):
        # Player 1
        die1,die2 = [random.randint(1,6),random.randint(1,6)]
        move = self.chooseMove(self.strategyA,die1,die2)
        self.makeMove(move) # Include a sanity check here perhaps
        if max(self.gamestate)<=0:
            return 1 # 1 for player 1 winning
        self.flipBoard()
        #Player 2
        die1,die2 = [random.randint(1,6),random.randint(1,6)]
        move = self.chooseMove(self.strategyB,die1,die2)
        self.makeMove(move)
        if max(self.gamestate)<=0:
            return -1 # -1 for player 2 winning
        self.flipBoard()
        return 0
        
    # The game environment
    def game(self):
        gameOver=0
        while not gameOver:
            gameOver = self.turn()
        if gameOver==1:
            print("Congrats to player 1!")
        else:
            print("Congrats to player 2!")

for i in range(1000):
    eddie = Board()
    eddie.game()
    print(i)


