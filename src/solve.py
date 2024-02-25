from utils import Note, pure_intervals, interval_weight
from params import WINSIZE
from scipy.linalg import solve_banded
import numpy as np

def tau(x: Note, y: Note):
    '''
    returns ideally desired interval between `x` and `y` in cents (positive if `x` has higher pitch than `y`)
    '''
    z = abs(x.semitones - y.semitones)
    z = pure_intervals[z%12] + z//12 * 1200
    return -z if x.semitones < y.semitones else z

def kappa(x: Note, y: Note):
    '''
    - returns the weight (importance factor) given to pair of notes `x` and `y`
    - order of parameters is unimportant
    '''
    timedif = x.start - y.end if x.start > y.start else y.start - x.end
    timedif = max(0, timedif)
    z = abs(x.semitones - y.semitones)
    return interval_weight[z%12] / (timedif+1)


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