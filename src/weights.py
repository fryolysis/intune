import numpy as np
from math import ceil
from intune.src.utils import msg_type

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

# TODO: implement a mixed strategy that takes into account both time proximity and frequency of occurrence

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
    if np.sum(weights) > 0:
        weights /= np.sum(weights)

    return weights


def __window_weight_update(weights, window):
    n = len(window)
    for i in range(n):
        for j in range(i+1,n):
            row = min(window[i]%12, window[j]%12)
            col = max(window[i]%12, window[j]%12)
            weights[row][col] = 1

def __window_slide(messages, weights, window_size, offset):
    window = []
    currently_playing_set = set()
    current_time = 0
    window_end = offset
    for msg in messages:
        current_time += msg.time
        # next window
        if current_time > window_end:
            __window_weight_update(weights, window)
            window = list(currently_playing_set)
            window_end = ceil((current_time-offset)/window_size)*window_size + offset
        if msg_type(msg) == 'on':
            currently_playing_set.add(msg.note)
            window.append(msg.note)
        else:
            currently_playing_set.remove(msg.note)
    # the case for last window
    __window_weight_update(weights, window)


def window_weight(messages, window_size=2):
    '''
    Window Weight
    =============
    - A measure of time proximity, frequency of occurrence is completely omitted.
    - Weight assigned is 1 if the pair of pitch class ever occurs within the window and 0 else. The window is slided throughout the score where step size is equal to `window_size`/2.
    '''

    weights = np.zeros([12,12])
    __window_slide(messages, weights, window_size, offset=0)
    __window_slide(messages, weights, window_size, offset=window_size/2)
    if np.sum(weights) > 0:
        weights /= np.sum(weights)
    return weights