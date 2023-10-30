import numpy as np

interval_weight = {
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 1,
    6: 0
}


def freq_weight(messages):
    '''
    weight of a pair of pitch class is defined to be the multiplication of freq of appeareance of each
    '''
    counters = np.zeros([12])
    weights = np.zeros([12,12])
    for msg in messages:
        if msg.type == 'on':
            counters[msg.note % 12] += 1
    
    # normalize
    counters /= np.sum(counters)

    for i in range(12):
        for j in range(i+1,12):
            weights[i][j] = counters[i] * counters[j]

    return weights

# TODO: define a weighting based on time proximity, and define a weighting based on a mixed strategy