# MIDI FACTS
# note range: 0-127 where 0 is C-1 and a step is a semitone
# pitch bend range -8191 to 8192, mapping to cents is unspecified
# channel range 0-15, pitch bend is applied to channels not notes
# ASSUMPTIONS
# output scale's first note is assumed to be C for convenience


from intune.src import solve, output, utils, weights
from sys import argv

assert len(argv) == 2, 'Please provide an input file in midi format.\n'
assert argv[1][-4:] == '.mid', 'Input file must have .mid extension'

score = utils.preprocess(argv[1])
pair_weights = weights.mixed_weight(score, window_size=0.1, alpha=1)
scale = solve.solve(pair_weights, weights.interval_weight)
output.scale_file(argv[1][:-4], scale)