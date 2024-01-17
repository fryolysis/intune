'''
generates mock music scores
'''
import random
from intune.src.utils import *


def from_pitch_set(pitch_set, length):
    '''
    - generates a random `Score` that may contain only the specified pitches
    - `pitch_set` must be in the range 0-11
    '''
    assert all([p in range(12) for p in pitch_set])
    notes = []
    pitch_set = [i+12*j for i in pitch_set for j in range(1,10)] # 11 + 12*9 = 119  < 127
    clock = 0
    for _ in range(length):
        n = Note(start=clock, startticks=round(clock), 
                 semitones=random.choice(pitch_set))
        n.halt(clock + random.random())
        notes.append(n)
        clock += random.random() # clock may be after or before the end of n
    return Score(notes)

def no_overlap(length):
    '''
    generates a random `Score` whose notes never sound simultaneously
    '''
    notes = []
    clock = 0
    for _ in range(length):
        n = Note(start=clock, startticks=round(clock),
                  semitones=random.randint(0,127))
        clock += random.random()
        n.halt(clock)
        notes.append(n)
        clock += random.random()
    return Score(notes)