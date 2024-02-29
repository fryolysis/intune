import numpy as np
from math import log2

MIDI_NOTE_COUNT = 128       # from midi standard
SUS_PEDAL_LIMIT = 64        # pedal on limit
WINSIZE = 30                # defines neighborhood of a note on one side (# of notes)

interval_weight = np.array([
    1e4,     # 0 - unison/octave
    0,
    0,
    0.1,      # 3 - min third
    1,      # 4 - maj third
    5,      # 5 - fourth
    0,      # 6 - devil's interval
    5,      # 7 - fifth
    0.01,
    0.01,
    0,0
], dtype=np.float64)


pure_ratios = [
    1/1,
    16/15,
    9/8,
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