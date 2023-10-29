from sys import argv
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

interval_weight = {
    '1': 0,
    '2': 0,
    '3': 1,
    '4': 1,
    '5': 1,
    '6': 0
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
    # TODO: ensure that it is a single track midi file
    messages = []
    for msg in MidiFile(argv[1]):
        mt = msg_type(msg)
        if mt == 'on' or mt == 'off':
            messages.append(msg)
    return messages