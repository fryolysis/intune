import numpy as np
from intune.src.utils import msg_type

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


#   WEIGHTS FOR PITCH CLASS PAIRS

def mixed_weight(messages, window_size=0.1, alpha=1):
    '''
    - Pairs which are more than `window_size` apart does not contribute to the calculation.
    - Weighting of a pair is proportional to k^`window_size` where k is the number of occurrence.
    '''
    relevant_past = [] # queue
    time_bag = 0
    weights = np.zeros([12,12])
    for msg in messages:
        time_bag += msg.time
        relevant_past.insert(0, msg)
        while time_bag > window_size:
            time_bag -= relevant_past.pop().time
        if msg_type(msg) == 'on':
            for m in relevant_past:
                if msg_type(m) == 'off':
                    weights[m.note%12][msg.note%12] += 1
    
    weights += weights.T
    weights **= alpha
    # normalize
    if np.sum(weights) > 0:
        weights /= np.sum(weights)
        
    return weights