# MIDI FACTS
# note range: 0-127 where 0 is C-1 and a step is a semitone
# pitch bend range -8191 to 8192, mapping to cents is unspecified
# channel range 0-15, pitch bend is applied to channels not notes

# output scale's first note is assumed to be C for convenience

import utils
import weights
import analytic


# MAIN
messages = utils.preprocess()
scale = analytic.solve(weights.freq_weight(messages), weights.interval_weight)

# output .scl file
with open('myscale.scl', 'w') as f:
    f.write('First note is C.\n')
    f.write(f'12\n') # num of lines
    for i in scale:
        f.write(f'{i}\n')
    f.write('2/1')