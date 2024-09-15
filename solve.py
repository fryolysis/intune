from utils import Note, desired_intervals, interval_weight
from params import *
from scipy.linalg import solve_banded
import numpy as np


def tau(x: Note, y: Note):
    '''
    returns ideally desired interval between `x` and `y` in cents (positive if `x` has higher pitch than `y`)
    '''
    z = abs(x.semitones - y.semitones)
    z = desired_intervals[z%12] + z//12 * 1200
    return -z if x.semitones < y.semitones else z


def kappa(x: Note, y: Note):
    '''
    - returns the weight (importance factor) given to pair of notes `x` and `y`
    - order of parameters is unimportant
    '''
    # special treatment in case both are key of piece
    if x.semitones%12 == KEY and y.semitones%12 == KEY:
        return 1e6
    # k>0 when two notes intersect and k is the time they sound together
    # k<0 when two notes does not intersect and -k is the time difference
    k = min(x.end, y.end) - max(x.start, y.start)
    z = abs(x.semitones - y.semitones)
    return max(interval_weight[z%12] * (k+GHOST), ZERO_WEIGHT)


def solve(score: list[Note]):
    '''
    prepares ab and b and solves Ax=b using SciPy's solve_banded function
    '''
    kappavecs = np.zeros([len(score), 2*WINSIZE+1])
    tauvecs = np.zeros([len(score), 2*WINSIZE+1])
    for i in range(len(score)):
        for j in range(-WINSIZE, WINSIZE+1):
            if j==0 or i+j < 0 or i+j >= len(score):
                continue
            kappavecs[i, j+WINSIZE] = kappa(score[i], score[i+j])
            tauvecs[i, j+WINSIZE] = tau(score[i], score[i+j])
    
    # vector b
    b = np.array([np.dot(k,t) for k,t in zip(kappavecs, tauvecs)]) 

    # matrix a
    a = lambda i,j: - kappavecs[i,j-i+WINSIZE] if i!=j else np.sum(kappavecs[i])
    # matrix ab
    ab = np.ndarray([2*WINSIZE+1, len(score)])
    for i in range(len(score)):
        for j in range(max(0,i-WINSIZE), min(len(score),i+WINSIZE+1)):
            ab[WINSIZE+i-j, j] = a(i,j)


    sol = solve_banded((WINSIZE, WINSIZE), ab, b, 
                 overwrite_ab=True, overwrite_b=True, check_finite=False)
    
    # shift the solution so that first note gets its default 12tet value
    default = score[0].semitones * 100
    sol += default - sol[0]
    # assign final values to notes
    for note, val in zip(score, sol):
        note.solution = val