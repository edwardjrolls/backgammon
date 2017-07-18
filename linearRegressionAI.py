import gammonAIbase as ai
import numpy as np
import linearRegression as lr
import board

# The class for the linear regression 
class LinearRegressionAI(ai.GammonAIbase):
    
    # Copies the initial state of the AIbase, and sets what 'features' we want to include
    def __init__(self,features='basic'):
        ai.GammonAIbase.__init__(self)
        self.features=features
        if self.features=='basic': # Set it up to have just the boring board state, giving effectively random moves
            self.beta=np.transpose(np.array([0.5]+[0]*26,ndmin=2))
        elif self.features=='extended': # Extended board state, which goes home pieces, home dead zone, away pieces, away dead zone
            self.beta=np.transpose(np.array([0.5]+[0]*50,ndmin=2))
            
    # Calculates the coefficients for a linear regression
    def calculateLinearRegressionCoefficients(self):
        #Regular state array if 'basic'
        if self.features=='basic':
            X = np.array(self.gameCollection['w']+self.gameCollection['l'])
            X = np.insert(X,0,1,axis=1)
        # Run the 'extendState' function for larger arrays
        elif self.features=='extended':
            extendedGameList=[]
            for state in self.gameCollection['w']+self.gameCollection['l']:
                extendedGameList.append(board.extendState(state))
            X = np.array(extendedGameList)
            X = np.insert(X,0,1,axis=1)
        y = np.transpose(np.array([1]*len(self.gameCollection['w'])+[0]*len(self.gameCollection['l']),ndmin=2))                
        self.beta = lr.linearRegressionNormalEquation(X,y)
            
if __name__=='__main__':
    e = LinearRegressionAI(features='extended')
    e.trainModel(10)
    e.calculateLinearRegressionCoefficients()
    print(e.beta)
    e.compareModels(100,strategyA='linRegression',strategyB='random',parametersA=[e.features,e.beta])
    
