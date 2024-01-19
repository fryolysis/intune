# always output .scl file with 0 cents corresponding to C
# if variable tuning flag is set, also output retuned version of input midi file

# TODO: calculate total cost after retuning to evaluate the value of variable tuning
# TODO: use numpy linear algebra to speed up solution

from intune.src import solve, output, weights, variable, preprocess, params
from sys import argv

prompt = '''
    usage:
    intune FILE [-r]

    -r flag is optional and if present, the input file will be tuned to the scale file. Note that in case where scale file contains more than 12 notes, the same midi semitone is tuned to different cent values during the score.
'''


if __name__ == '__main__':
    if len(argv) == 3:
        _, fpath, mode = argv
        assert mode == '-r', 'Invalid parameter'
        mode = 'retune'
    elif len(argv) == 2:
        _, fpath = argv
        mode = 'scale'
    else:
        raise ValueError(prompt)

    assert fpath[-4:] == '.mid', 'Input file must have .mid extension'
    score, mfile = preprocess.preprocess(fpath)
    variable.tuningpoints(score)
    pair_weights = weights.mixed_weight(score)
    solve.solve(score, pair_weights)
    output.output_scl(fpath, score)
    if mode == 'retune':
        output.output_midi(mfile, fpath, score)