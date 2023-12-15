from mido import MidiFile

SUS_PEDAL_LIMIT = 64 # >=64 is pedal on
# from midi standard
MIDI_NOTE_COUNT = 128

# cents
pure_intervals = {
    1: 112,   # 16/15
    2: 204,   # 9/8
    3: 316,   # 6/5
    4: 386,   # 5/4
    5: 498,   # 4/3
    6: 590,   # 45/32
}

for i in range(1,6):
    pure_intervals[12-i] = 1200 - pure_intervals[i]


def msg_type(msg):
    if msg.type == 'note_off':
        return 'off'
    elif msg.type == 'note_on':
        return 'off' if msg.velocity == 0 else 'on'
    elif msg.type == 'control_change' and msg.control == 64:
        return 'sustain_off' if msg.value < SUS_PEDAL_LIMIT else 'sustain_on'
    else:
        return msg.type

class Note:
    def __init__(self, start, semitones):
        self.start = start
        self.semitones = semitones
        self.cls = semitones % 12
    def halt(self, end):
        self.end = end


class Score:
    def __init__(self, notelist):
        self.notes = notelist


def preprocess(filename):
    '''
    - Sustain pedals are converted into prolonged note duration. If a note is played more than once while pedal is down, it goes off and on again immediately.
    - All other messages are ignored. Score object is created.
    - All channels are united into one and if there are overlapping notes with the same midi note attribute we take their union and consider them as a single note.
    '''
    messages = MidiFile(filename)
    clock = 0
    notes = []
    note_ctr = [0]*MIDI_NOTE_COUNT
    pressednotes = [None]*MIDI_NOTE_COUNT
    sustainednotes = [None]*MIDI_NOTE_COUNT
    sustain_on = False

    for msg in messages:
        clock += msg.time if msg.time else 0
        t = msg_type(msg)

        # a note pressed
        if t == 'on' and note_ctr[msg.note] == 0:
            # check if the note is sustained before
            m = sustainednotes[msg.note]
            m.halt(clock) if m else None
            n = Note(start=clock, semitones=msg.note)
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

    return Score(notes)
