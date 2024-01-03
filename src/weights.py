import numpy as np
from collections import deque

interval_weight = np.array([
    0,0,0,
    0.1,    # 3 - min third
    1,      # 4 - maj third
    1,      # 5 - fourth
    0,
    5,      # 7 - fifth
    0,0,0,0
], dtype=np.float128)


# weighting scheme

def mixed_weight(score, window_size=0.1, alpha=1):
    '''
    - Pairs which are more than `window_size` apart does not contribute to the calculation.
    - Weighting of a pair is proportional to k^`window_size` where k is the number of occurrence.
    '''
    # queue of recent elements, left-end is the most recent
    q = deque()
    weights = np.zeros([12,12])
    for note in score.notes:
        q.appendleft(note)
        while note.start - q[-1].end > window_size:
            q.pop()
        for pnote in q:
            weights[pnote.cls][note.cls] += 1
    
    weights += weights.T
    weights **= alpha

    return weights