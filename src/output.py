import mido
from intune.src.params import *


comma1, comma2 = 100/128, 100/16384
'''
FORMAT OF MIDI TUNING CHANGE SYS MESSAGE
-----------------

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

# BUG: sometimes the tuning is an octave higher than it should be

def _get_all(_cls, semshift):
    validrange = lambda n: n<128 and n>=0
    ls1 = [_cls + n*12 for n in range(11)]
    return [(n, n+semshift) for n in ls1 if
            validrange(n) and validrange(n+semshift)]

def _get_payload(note, cents_in_oct):
    '''
    tunes the pitch class in all octaves
    '''
    val = (note.semitones//12)*1200 + cents_in_oct
    xx, rem = val//100, val%100
    yy, rem2 = rem//comma1, rem%comma1
    zz = rem2//comma2
    tuples = _get_all(note.cls, xx - note.semitones)
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
    cls_to_lastid = [-1]*12 # -1 is not a valid id
    for note in score.notes:
        # if id of that cls is changed then retune
        if cls_to_lastid[note.cls] != note.varid:
            cls_to_lastid[note.cls] = note.varid
            payload = _get_payload(note, score.solution[note.varid])
            # put 1 tick earlier if possible
            delay = max(note.startticks - oldticks - 1, 0)
            msg = mido.Message('sysex', data=payload, time=delay)
            trk.append(msg)
            oldticks = note.startticks
    
    mfile.tracks.append(trk)
    mfile.type = 1
    mfile.save(fpath[:-4] + '-retuned.mid')


def _sol_to_scl(score):
    '''
    - includes at least one pitch for each pitch class and outputs a list in ascending order
    - missing pitch classes are assigned to their default value where

    C --> 0
    C# --> 100
    ...
    '''
    scl = []
    cls_in_sol = [i//K for i in score.solution.keys()]
    for i in range(12):
        if i not in cls_in_sol:
            scl.append(i*100)
    scl += list(score.solution.values())
    scl.sort()
    return scl[1:]  # discard 0 cents, which is guaranteed to exist

def output_scl(fname, score):
    scale = _sol_to_scl(score)
    with open(fname[:-4]+'.scl', 'w') as f:
        f.write('First note is C\n')
        f.write(f'{len(scale)+1}\n') # num of lines
        for cents in scale:
            f.write(f'{cents:.1f}\n')
        f.write('2/1')