# variable tuning 

import solve, output, utils, plot
from params import *
from sys import argv
from os.path import basename

assert argv[1][-4:] == '.mid', 'Input file must have .mid extension'
piece_name = basename(argv[1])[:-4]

score, mfile = utils.preprocess(argv[1])
solve.solve(score)
output.output_midi(mfile, argv[1], score)
plot.plot(score, f'{piece_name}')

# # experiment
# for i in [1,100]:
#     interval_weight[0] = i
#     solve.solve(score)
#     plot.plot(score, f'{piece_name}: unison/octave weight = {i}')