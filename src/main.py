# MIDI FACTS
# note range: 0-127 where 0 is C-1 and a step is a semitone
# pitch bend range -8191 to 8192, mapping to cents is unspecified
# channel range 0-15, pitch bend is applied to channels not notes
# ASSUMPTIONS
# output scale's first note is assumed to be C for convenience


from intune.src import solve, output, utils, weights, variable
from sys import argv

prompt = '''
    usage:
    intune FILE MODE

    MODE:
        -f: fixed mode
        -v: variable mode
'''

def fixedmode(score, winsize=.1):
    pair_weights = weights.mixed_weight(score, winsize)
    solve.solve(score, pair_weights, weights.interval_weight)
    

def varmode(score, winsize=.1, forgetbef=100):
    variable.tuningpoints(score, forgetbef)
    pair_weights = variable.mixed_weight_var(score, winsize)
    variable.solve_var(score, pair_weights, weights.interval_weight)

if __name__ == '__main__':
    assert len(argv) == 3, prompt
    _, fpath, mode = argv
    assert fpath[-4:] == '.mid', 'Input file must have .mid extension'

    score, mfile = utils.preprocess(fpath)
    if mode == '-f':
        fixedmode(score)
        output.scale_file(fpath[:-4], score.solution)
    elif mode == '-v':
        varmode(score)
        variable.output_midi(mfile, fpath, score)
        variable.printscale(score.solution)
    else:
        raise ValueError('invalid mode flag')