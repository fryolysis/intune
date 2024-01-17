from mido import MidiFile
from intune.src.typedefs import *
from math import log2

SUS_PEDAL_LIMIT = 64 # >=64 is pedal on
# from midi standard
MIDI_NOTE_COUNT = 128

pure_ratios = [
    1/1,
    13/12,
    8/7,
    6/5,
    5/4,
    4/3,
    7/5,
    3/2,
    8/5,
    5/3,
    9/5,
    15/8,
]
# cents
pure_intervals = [log2(r)*1200 for r in pure_ratios]


def msg_type(msg):
    if msg.type == 'note_off':
        return 'off'
    elif msg.type == 'note_on':
        return 'off' if msg.velocity == 0 else 'on'
    elif msg.type == 'control_change' and msg.control == 64:
        return 'sustain_off' if msg.value < SUS_PEDAL_LIMIT else 'sustain_on'
    else:
        return msg.type


def preprocess(filename):
    '''
    - Sustain pedals are converted into prolonged note duration. If a note is played more than once while pedal is down, it goes off and on again immediately.
    - All other messages are ignored. Score object is created.
    - All channels are united into one and if there are overlapping notes with the same midi note attribute we take their union and consider them as a single note.
    '''
    mfile = MidiFile(filename)
    clock, ticks = 0,0
    notes = []
    note_ctr = [0]*MIDI_NOTE_COUNT
    pressednotes = [None]*MIDI_NOTE_COUNT
    sustainednotes = [None]*MIDI_NOTE_COUNT
    sustain_on = False

    for msg, msgorig in zip(mfile, mfile.merged_track, strict=True):
        clock += msg.time if msg.time else 0
        ticks += msgorig.time if msgorig.time else 0
        t = msg_type(msg)

        # a note pressed
        if t == 'on' and note_ctr[msg.note] == 0:
            # check if the note is sustained before
            m = sustainednotes[msg.note]
            m.halt(clock) if m else None
            n = Note(start=clock, startticks=ticks, semitones=msg.note)
            pressednotes[msg.note] = n
            notes.append(n) # notes are ordered wrt their pressing time

        # a note released
        elif t == 'off' and note_ctr[msg.note] == 1:
            n = pressednotes[msg.note]
            if sustain_on:
                sustainednotes[msg.note] = n
            else:
                n.halt(clock)
        if t == 'on':
            note_ctr[msg.note] += 1
        elif t =='off':
            note_ctr[msg.note] -= 1
        elif t == 'sustain_on':
            sustain_on = True
        elif t == 'sustain_off':
            # halt all sustained notes
            [n.halt(clock) for n in sustainednotes if n]
            sustain_on = False
            
    # in case the song ends with sustain pedal on, halt all notes
    if sustain_on:
        [n.halt(clock) for n in sustainednotes if n]

    return Score(notes), mfile
