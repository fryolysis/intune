
def align(sol):
    '''
    - Assuming that no note moves more than 100 cents from its default 12tet location, ordering of notes will be correct.
    - There is always a note that is assigned to 0 cents, which is required for .scl standard. That note is always chosen to be C for convenience.
    '''
    
    # iterates over C, C#, D.. until it finds one that's in the solution
    for i in range(12):
        if i in sol:
            akey = i
            break
    # shift all notes so that the picked note gets its default 12-tet value                   
    sol = {k : (v-sol[akey]+akey*100)%1200 
            for k,v in sol.items()
    }

    # use 12tet default vals of missing pitches if there any
    scl = []
    for i in range(1,12):
        scl.append(
            sol[i] if i in sol else i*100
        )
    return scl

def scale_file(fname, scale):
    with open(fname+'.scl', 'w') as f:
        f.write('First note is C.\n')
        f.write('12\n') # num of lines
        for cents in scale:
            f.write(f'{cents:.1f}\n')
        f.write('2/1')

def midi_file(fname, midi_messages):
    pass