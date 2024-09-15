import numpy as np

MIDI_NOTE_COUNT = 128       # from midi standard
SUS_PEDAL_LIMIT = 64        # pedal on limit (0-127)
WINSIZE = 80                # defines neighborhood of a note on one side (# of notes)
GHOST = 0                   # length of ghost part of a note in time difference calculations, useful for monophonic music
WINSIZE = 80                # defines neighborhood of a note on one side (# of notes)
GHOST = 0                   # length of ghost part of a note in time difference calculations, useful for monophonic music
ZERO_WEIGHT = 1e-6          # exact 0 may cause singular matrix problems
KEY = None                  # it's computed from score

interval_weight = np.array([
    50,    # 0 - unison/octave
    0,
    0,
    1e-3,    # 3 - min third
    1,       # 4 - maj third
    5,       # 5 - fourth
    0,       # 6 - devil's interval
    5,       # 7 - fifth
    1e-3,
    1e-3,
    0,0
], dtype=np.float64)

# cents
desired_intervals = [
    0,
    100,
    200,
    316,
    386,
    498,
    600,
    702,
    1200-386,
    1200-316,
    1000,
    1100,
]