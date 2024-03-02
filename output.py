import mido
from params import *
from utils import Note

COMMA1, COMMA2 = 100/128, 100/16384
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

def _get_payload(note):
    '''
    prepares the sysex midi message that tunes `note`
    '''
    xx, rem = int(note.solution//100), note.solution%100
    yy, rem2 = int(rem//COMMA1), rem%COMMA1
    zz = int(rem2//COMMA2)
    return (127, 127, 8, 2, 0, 1, note.semitones, xx, yy, zz)


def output_midi(mfile: mido.MidiFile, fpath, score: list[Note]):
    '''
    prepares sysex messages and adds them as a tuning track to the original midi file and then saves the new file
    '''
    if mfile.type == 2:
        raise ValueError('Type-2 midi files are not supported')
    mfile.type = 1  # to convert type-0 files
    
    # insert dummy message in front of all other tracks to shift them forward by 1 tick. This is done to be able to tune first notes in case they start at first tick
    for t in mfile.tracks:
        t.insert(0, mido.Message('sysex', time=1))

    # tuning track
    trk = mfile.add_track('tuning')
    # tuning message will arrive 1 tick before the tuned note
    oldticks = 1

    for note in score:
        note.startticks += 1 # update startticks
        payload = _get_payload(note)
        delay = note.startticks - oldticks
        msg = mido.Message('sysex', data=payload, time=delay)
        trk.append(msg)
        oldticks = note.startticks
    
    mfile.save(fpath[:-4] + '-retuned.mid')