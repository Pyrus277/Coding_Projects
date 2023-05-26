import pprintpp as pp
import numpy as np

def calculate(list):
    '''
    Take a list 9 items long and converts to a 3x3 numpy array.
    Returns mean, variance, stdev, max, min, and sum, each 
    across both axes and also flattened, in a dictionary
    '''
    calculations = dict()

    
    try:
        list = np.reshape(list, (3,3))
    except ValueError: 
        raise ValueError("List must contain nine numbers.")

    calculations['mean'] = \
        [np.mean(list, axis=0).tolist(), 
         np.mean(list, axis=1).tolist(), 
         np.mean(list)]

    calculations['variance'] = \
        [np.var(list, axis=0).tolist(), 
         np.var(list, axis=1).tolist(), 
         np.var(list)]
    
    calculations['standard deviation'] = \
        [np.std(list, axis=0).tolist(), 
         np.std(list, axis=1).tolist(), 
         np.std(list)]
    
    calculations['max'] = \
        [np.amax(list, axis=0).tolist(), 
         np.amax(list, axis=1).tolist(), 
         np.amax(list)]

    calculations['min'] = \
        [np.amin(list, axis=0).tolist(), 
         np.amin(list, axis=1).tolist(), 
         np.amin(list)]
    
    calculations['sum'] = \
        [np.sum(list, axis=0).tolist(), 
         np.sum(list, axis=1).tolist(), 
         np.sum(list)]

    return calculations


if __name__=='__main__':
    list = [0,1,2,3,4,5,6,7,8,9]
    pp.pprint(calculate(list))
          