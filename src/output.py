

def scale_label(scale):
    text = ''
    for cents in scale:
        text += f'{cents:.1f}\n'
    return text

def scale_file(fname, scale):
    with open(fname, 'w') as f:
        f.write('First note is C.\n')
        f.write('12\n') # num of lines
        for cents in scale:
            f.write(f'{cents:.1f}\n')
        f.write('2/1')

def midi_file(fname, midi_messages):
    pass