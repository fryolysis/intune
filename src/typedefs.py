class Note:
    def __init__(self, start, semitones, startticks):
        self.start = start
        self.startticks = startticks
        self.semitones = semitones
        self.cls = semitones % 12
    def halt(self, end):
        self.end = end
    def setvarid(self, varid):
        self.varid = varid



class Score:
    '''
    - `notes`:              a list of Note objects in the order of note_on
    - `solution`:           a dict that maps variable ids to tuned cent values
    - `varid_to_note`:      a dict that maps variable ids to the first note objects assigned to them
    '''
    def __init__(self, notelist):
        self.notes = notelist
        self.solution = None
        self.varid_to_note = None