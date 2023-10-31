
def scale_file(fname, scale):
    with open(f'{fname}.scl', 'w') as f:
        f.write('First note is C.\n')
        f.write(f'12\n') # num of lines
        for cents in scale:
            f.write(f'{cents:.1f}\n')
        f.write('2/1')

def midi_file(fname, midi_messages):
    pass