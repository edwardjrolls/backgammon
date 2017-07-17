# Runs linear regression on a list of lists, outputs a 
import numpy as np

# Runs linear regression via the normal equation method
def linearRegressionNormalEquation(X,y):
    gramMat = np.matmul(np.transpose(X),X)
    momMat = np.matmul(np.transpose(X),y)
    beta = np.linalg.solve(gramMat,momMat)
    return beta

