from mido import MidiFile



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
    else:
        return msg.type


def preprocess(filename):
    '''
    checks for validity of midi file and discards system messages
    '''
    midifile = MidiFile(filename)

    messages = []
    time_bag = 0
    for msg in midifile:
        if msg.type in ['note_on', 'note_off']:
            msg.time += time_bag
            time_bag = 0
            messages.append(msg)
        elif msg.time:
            time_bag += msg.time
    return messages