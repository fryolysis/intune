import numpy as np
from utils import msg_type
from math import ceil

interval_weight = {
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 1,
    6: 0
}
for i in range(1,6):
    interval_weight[12-i] = interval_weight[i]


#   WEIGHTS FOR PITCH CLASS PAIRS

def freq_weight(messages):
    '''
    Weight of a pair of pitch class is defined to be the relative freq of its number of occurrence.
    '''
    counters = np.zeros([12])
    weights = np.zeros([12,12])
    for msg in messages:
        if msg_type(msg) == 'on':
            counters[msg.note % 12] += 1


    for i in range(12):
        for j in range(i+1,12):
            weights[i][j] = counters[i] * counters[j]

    # normalize
    weights /= np.sum(weights)

    return weights


def time_weight(messages):
    '''
    Time Weight
    ============
    - Weight of a pair of pitch class is inversely proportional to their least distance in time. 
    - Completely omits frequency of occurrence.
    '''
    pass

def __window_weight_update(weights, window):
    n = len(window)
    for note1 in range(n):
        for note2 in range(i+1,n):
            weights[note1 % 12][note2 % 12] += 1

def window_weight(messages, window_size=300):
    '''
    Window Weight
    =============
    A mixture of time proximity and frequency of occurence. Weight of a pair of pitch class is proportional to the number of times they sound together in a time window of size `window_size`, slided all through the score.

    Equivalent to `freq_weight` when `window_size` is larger than the length of the piece.
    '''
    # FIXME does not agree with freq_weight! something is wrong!

    weights = np.zeros([12,12])
    window = []
    currently_playing_set = set()
    current_time = 0
    window_end = window_size
    for msg in messages:
        current_time += msg.time
        # next window
        if current_time > window_end:
            __window_weight_update(weights, window)
            window = list(currently_playing_set)
            window_end = ceil(current_time/window_size)*window_size
        if msg_type(msg) == 'on':
            currently_playing_set.add(msg.note)
            window.append(msg.note)
        else:
            currently_playing_set.remove(msg.note)
    # the case for last window
    __window_weight_update(weights, window)

    weights /= np.sum(weights)
    return weights