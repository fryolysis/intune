from intune.src.params import *
from sklearn.cluster import KMeans
from collections import deque
import numpy as np


def tuningpoints(score):
    '''
    - a vector of neighborhood is constructed for each note in the score
    - applies k-means clustering for each pitch class. at the end we will have at most 12*k notes in the scale
    '''

    notespercls = [[] for _ in range(12)]

    # queue of recent elements, left-end is the most recent
    q = deque()
    for note in score.notes:
        notespercls[note.cls].append(note)
        q.appendleft(note)
        while note.start - q[-1].end > WINSIZE/2:
            q.pop()
        # don't count self
        it = iter(q)
        next(it)
        for pnote in it:
            note.nbhood[pnote.cls] = 1
            pnote.nbhood[note.cls] = 1
    
    # nbhood computation is done, now compute clusters for each pitch class and assign unique varid's
    for i in range(12):
        notes = notespercls[i]
        vecs = np.array([n.nbhood for n in notes])
        res = KMeans(K, n_init='auto').fit(vecs)
        for j in range(len(vecs)):
            notes[j].varid = res.labels_[j] + i*K
        