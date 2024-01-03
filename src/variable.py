from intune.src.weights import *
import sympy, mido
from intune.src.utils import pure_intervals

comma1, comma2 = 100/128, 100/16384
'''
F0 7F id 08 02 tt ll [kk xx yy zz]x(ll) F7
where

F0 7F = universal realtime SysEx header
id    = target device ID
08    = sub-id #1 (MIDI tuning standard)
02    = sub-id #2 (note change)
tt    = tuning program number from 0 to 127
ll    = number of notes to be changed (sets of [kk xx yy zz])
[kk xx yy zz] = MIDI note number, followed by frequency data for note
F7    = end of SysEx message


xx = semitone (MIDI note number to retune to, unit is 100 cents)
yy = MSB of fractional part (1/128 semitone = 100/128 cents = .78125 cent units)
zz = LSB of fractional part (1/16384 semitone = 100/16384 cents = .0061 cent units)

7F 7F 7F is reserved for no change to the existing note tuning
'''

def get_all(_cls, semshift):
    validrange = lambda n: n<128 and n>=0
    ls1 = [_cls + n*12 for n in range(11)]
    return [(n, n+semshift) for n in ls1 if
            validrange(n) and validrange(n+semshift)]

def get_payload(note, cents_in_oct):
    '''
    tunes the pitch class in all octaves
    '''
    val = (note.semitones//12)*1200 + cents_in_oct
    xx, rem = val//100, val%100
    yy, rem2 = rem//comma1, rem%comma1
    zz = rem2//comma2
    tuples = get_all(note.cls, xx - note.semitones)
    appendix = () 
    for a in [t+(yy,zz) for t in tuples]:
        appendix += a
    return (127, 127, 8, 2, 0, len(tuples)) + appendix

def output_midi(mfile, fpath, score):
    '''
    prepares sysex messages and add them as a tuning track to the original midi file and then saves the new file
    - one pitch class is changed as a whole in a message
    '''
    # new track
    trk = []
    oldticks = 0
    for varid, note in enumerate(score.varid_to_note):
        payload = get_payload(note, score.solution[varid])
        # put 1 tick earlier if possible
        delay = max(note.startticks - oldticks - 1, 0)
        msg = mido.Message('sysex', data=payload, time=delay)
        oldticks = note.startticks
        trk.append(msg)
    
    mfile.tracks.append(trk)
    mfile.save(fpath[:-4] + '-retuned.mid')

def align_var(score, sol):
    '''
    - There is always a note that is assigned to 0 cents, which is required for .scl standard. That note is always chosen to be C for convenience.
    '''
    idtocls = [note.cls for note in score.varid_to_note]
    # if C is in the solution pick it, otherwise pick an arbitrary note
    akey = idtocls.index(0) if 0 in idtocls else next(iter(sol))
    # shift all notes so that the picked note gets its default 12-tet value
    sol = {k : (v-sol[akey]+idtocls[akey]*100)%1200 for k,v in sol.items()}
    return sol

def printscale(sol):
    for cents in sorted(sol.values()):
        print(cents)

# TODO: implement a more sophisticated tuning algorithm, preferably one that employs a clustering algorithm
def tuningpoints(score, forgetbefore=10):
    lastnote = [None]*12
    varid_to_note = []
    varid = -1
    for note in score.notes:
        # add new tuning point if the last instance of that class is forgotten
        if not lastnote[note.cls] or note.start - lastnote[note.cls].end > forgetbefore:
            varid_to_note.append(note)
            varid += 1
            note.setvarid(varid)
        else:
            note.setvarid( lastnote[note.cls].varid )
        lastnote[note.cls] = note
    
    score.varid_to_note = varid_to_note

def mixed_weight_var(score, window_size=3, alpha=1):
    '''
    - Pairs which are more than `window_size` apart does not contribute to the calculation.
    - Weighting of a pair is proportional to k^`window_size` where k is the number of occurrence.
    '''
    varcount = len(score.varid_to_note)
    # queue of recent elements, left-end is the most recent
    q = deque()
    weights = np.zeros([varcount, varcount])
    for note in score.notes:
        q.appendleft(note)
        while note.start - q[-1].end > window_size:
            q.pop()
        for pnote in q:
            weights[pnote.varid][note.varid] += 1
    
    weights += weights.T
    weights **= alpha

    return weights


def solve_var(score, pitch_pair_weights, interval_weights):
    varcount = pitch_pair_weights.shape[0]
    x = list( sympy.symbols(f':{varcount}') )
    # loss function
    L = sympy.S.Zero
    for i in range(varcount):
        for j in range(i+1, varcount):
            icls, jcls = score.varid_to_note[i].cls, score.varid_to_note[j].cls
            big,smol,clsdiff = (i,j,icls-jcls) if icls > jcls else (j,i,jcls-icls)
            L += pitch_pair_weights[i][j] * interval_weights[clsdiff] * (x[big]-x[smol]-pure_intervals[clsdiff])**2
    # partial derivatives
    eqns = []
    for i in range(varcount):
        eqns.append( L.diff(x[i]) )
    # solve
    sol = sympy.solve(eqns, x)
    
    # in case of no solution abort
    assert sol, "No solution, aborting.."
    
    # normally the rank of the matrix must be at most 11 so there shouldn't be a unique solution (loss function is translation invariant). However due to floating point errors we usually have a unique solution.
    # assuming there is always a unique solution
    try:
        # get rid of sympy symbols
        sol = {int(str(k)) : v for k,v in sol.items()} 
    except AssertionError():
        print('solution is not unique!')
    
    score.solution = align_var(score, sol)