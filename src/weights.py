import numpy as np
from collections import deque
from intune.src.params import *


# weighting scheme

def mixed_weight(score):
    '''
    - Pairs which are more than `WINSIZE` apart does not contribute to the calculation.
    - Weighting of a pair is proportional to c^`ALPHA` where c is the number of occurrence.
    '''
    varcount = K*12
    # queue of recent elements, left-end is the most recent
    q = deque()
    weights = np.zeros([varcount, varcount])
    for note in score.notes:
        q.appendleft(note)
        while note.start - q[-1].end > WINSIZE/2:
            q.pop()
        for pnote in q:
            weights[pnote.varid][note.varid] += 1
    
    weights += weights.T
    weights **= ALPHA

    return weights