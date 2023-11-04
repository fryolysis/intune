'''
generates mock music scores
'''
import random, mido

def from_pitch_set(pitch_set, length):
    '''
    - generates random scores that contain only the specified pitch classes
    - `pitch_set` must be in the range 0-11
    - `length` is only expected, the real length can be longer or shorter
    '''
    assert all([p in range(12) for p in pitch_set])
    res = []
    msg_set = []
    pitch_set = [i+12*j for i in pitch_set for j in range(1,10)] # 11 + 12*9 = 119  < 127
    for _ in range(2*length):
        if random.random() > .5:
            pickables = [i for i in pitch_set if i not in msg_set]
            if not pickables:
                continue
            note = random.choice(pickables)
            msg_set.append(note)
            on = mido.Message.from_dict({
                'type': 'note_on',
                'note': note,
                'time': random.random()
            })
            res.append(on)
        elif msg_set:
            note = random.choice(msg_set)
            msg_set.remove(note)
            off = mido.Message.from_dict({
                'type': 'note_off',
                'note': note,
                'time': random.random()
            })
            res.append(off)
    for m in msg_set:
        off = mido.Message.from_dict({
            'type': 'note_off',
            'note': m,
            'time': random.random()
        })
        res.append(off)
    return res

def no_overlap(length):
    '''
    generates random scores whose notes never sound simultaneously
    '''
    res = []
    for _ in range(length):
        note = random.randint(0,127)
        on = mido.Message.from_dict({
            'type': 'note_on',
            'note': note,
            'time': 1
        })
        off = mido.Message.from_dict({
            'type': 'note_off',
            'note': note,
            'time': 1
        })
        res += [on, off]
    return res