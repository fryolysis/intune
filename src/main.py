# variable tuning 

import solve, output, utils
from sys import argv

assert argv[1][-4:] == '.mid', 'Input file must have .mid extension'
score, mfile = utils.preprocess(argv[1])
solve.solve(score)
output.output_midi(mfile, argv[1], score)