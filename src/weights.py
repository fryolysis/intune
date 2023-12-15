import numpy as np
from collections import deque

interval_weight = {
    1: 0.01,
    2: 0.01,
    3: 0.1,
    4: 1,
    5: 3,
    6: 0
}

for i in range(1,6):
    interval_weight[12-i] = interval_weight[i]


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
        for pnote in [q[i] for i in range(1, len(q))]:
            weights[pnote.cls][note.cls] += 1
    
    weights += weights.T
    weights **= alpha
    # normalize
    if np.sum(weights) > 0:
        weights /= np.sum(weights)
        
    return weights