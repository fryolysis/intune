from mido import MidiFile, Message

SUS_PEDAL_LIMIT = 64 # >=64 is pedal on

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


def preprocess(filename):
    '''
    1. Only the first `note_on` and the last `note_off` messages are considered for a particular note in a particular channel.
    1. All other messages are discarded, total time of those that have time attribute are added to the next non-discarded message.
    1. Sustain pedals are converted into prolonged note duration. If a note is played more than once while pedal is down, it goes off and on again immediately.
    '''
    messages = MidiFile(filename)
    stages = [
        __handle_multiple_note_ons,
        __process_sustain_pedal,
        __discard_others
    ]
    for s in stages:
        messages = s(messages)
    return messages


def __handle_multiple_note_ons(messages):
    note_ctr = [0]*128
    res = []
    for msg in messages:
        t = msg_type(msg)
        if (t == 'on' and note_ctr[msg.note] == 0) or \
            (t == 'off' and note_ctr[msg.note] == 1):
            res.append(msg)
        if t == 'on':
            note_ctr[msg.note] += 1
        elif t == 'off':
            note_ctr[msg.note] -= 1
        else:
            res.append(msg)
    return res

def __process_sustain_pedal(messages):
    pedal_on = False
    pending_note_offs = []
    time_bag = 0
    res = []
    for msg in messages:
        t = msg_type(msg)
        if t == 'off' and pedal_on:
            time_bag += msg.time
            msg.time = 0
            pending_note_offs.append(msg)  
        else:
            msg.time += time_bag
            time_bag = 0
            # if a note is played again while pedal is down, play it
            if t == 'on' and msg.note in [i.note for i in pending_note_offs]:
                res.append( Message(type='note_off', time=msg.time, note=msg.note) )
                msg.time = 0
            res.append(msg)        
            if t == 'sustain_on':
                pedal_on = True
            elif t == 'sustain_off':
                res += pending_note_offs
                pending_note_offs.clear()
                pedal_on = False
    return res

def __discard_others(messages):
    time_bag = 0
    res = []
    for msg in messages:
        if msg.type in ['note_on', 'note_off']:
            msg.time += time_bag
            time_bag = 0
            res.append(msg)
        elif msg.time:
            time_bag += msg.time
    return res
