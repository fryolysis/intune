import numpy as np

class Note:
    '''
    abs time: time passed since a fixed point back in time (start of the song)
    - `start`:      abs time of start of note
    - `startticks`: ticks version of `start`
    - `end`:        abs time of end of note
    - `semitones`:  note field of midi standard (0-127)
    - `cls`:        pitch class (0-12)
    - `nbhood`:     a 12d vector defining the neighborhood
    - `varid`:      variable id
    '''
    def __init__(self, start, semitones, startticks):
        self.start = start
        self.startticks = startticks
        self.end = None
        self.semitones = semitones
        self.cls = semitones % 12
        self.nbhood = np.zeros([12], dtype=float)
        self.varid = None



class Score:
    '''
    - `notes`:              a list of Note objects in the order of note_on
    - `solution`:           a dict that maps variable ids to tuned cent values
    '''
    def __init__(self, notelist):
        self.notes = notelist
        self.solution = None