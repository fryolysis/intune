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
    def __init__(self, notelist):
        # in the order of note_on
        self.notes = notelist
        # maps varid to cents
        self.solution = None
        # maps each varid to the first note instance it is assigned to
        self.varid_to_note = None