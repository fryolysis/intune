import numpy as np
from math import log2

MIDI_NOTE_COUNT = 128       # from midi standard
SUS_PEDAL_LIMIT = 64        # >=64 is pedal on
K = 2                       # for K-means clustering
WINSIZE = .1                # defines neighborhood of a note (secs)
ALPHA = 1                   # importance of occurrence frequency (alpha > 0)

interval_weight = np.array([
    0,0,0,
    0.1,    # 3 - min third
    2,      # 4 - maj third
    3,      # 5 - fourth
    0,
    5,      # 7 - fifth
    1,
    0.1,
    0,0
], dtype=np.float128)


pure_ratios = [
    1/1,
    13/12,
    8/7,
    6/5,
    5/4,
    4/3,
    7/5,
    3/2,
    8/5,
    5/3,
    9/5,
    15/8,
]

# cents
pure_intervals = [log2(r)*1200 for r in pure_ratios]