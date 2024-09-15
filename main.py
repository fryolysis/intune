# variable tuning 

import solve, output, utils, plot, key
from params import *
from sys import argv
from os.path import basename

assert argv[1][-4:] == '.mid', 'Input file must have .mid extension'
piece_name = basename(argv[1])[:-4]

score, mfile = utils.preprocess(argv[1])
KEY = key.deduce_key(score)
solve.solve(score)
output.output_midi(mfile, argv[1], score)
plot.error_report(score)
plot.plot(score, f'{piece_name}')