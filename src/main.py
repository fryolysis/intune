# MIDI FACTS
# note range: 0-127 where 0 is C-1 and a step is a semitone



# given a piece in midi format, proposes a good temperament for it

# Intervals that taken into account are minor-major 3rds and perfect 5th. Their octave complement are automatically handled.

# The idea is to define a sum-of-squares loss and minimize it.
# Loss of a score is defined as the weighted sum of sqares of deviations from the pure interval, which is 3/2 for fifths, 5/4 for major thirds and 6/5 for minor thirds.
# The problem is easy to solve analytically, it just boils down to a system of linear equations with at most 11 unknowns.

import utils
import weights



# TODO: make more options and allow user to choose one
def pitch_pair_weights(messages):
    weights.freq_weight(messages)


def solve(weights):
    pass


# MAIN
if len(utils.argv) != 2:
    print('Please provide an input file in midi format')
    exit(1)

messages = utils.preprocess()
weights = pitch_pair_weights(messages)
scale = solve(weights)