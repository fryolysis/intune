from sys import argv, stderr
from mido import MidiFile



OCTAVE_CENTS = 1200

# cents
pure_intervals = {
    '1': 112,   # 16/15
    '2': 204,   # 9/8
    '3': 316,   # 6/5
    '4': 386,   # 5/4
    '5': 498,   # 4/3
    '6': 590,   # 45/32
}


def msg_type(msg):
    if msg.type == 'note_off':
        return 'off'
    elif msg.type == 'note_on':
        return 'off' if msg.velocity == 0 else 'on'
    else:
        return msg.type


def preprocess():
    '''
    checks for validity of midi file and discards system messages
    '''
    if len(argv) != 2:
        print('Please provide an input file in midi format.', file=stderr)
        exit(1)

    midifile = MidiFile(argv[1])
    if midifile.type != 1:
        print('Midi file must contain a single track.', file=stderr)
        exit(1)

    messages = []
    for msg in midifile:
        mt = msg_type(msg)
        if mt == 'on' or mt == 'off':
            messages.append(msg)
    return messages