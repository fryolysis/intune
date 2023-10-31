# MIDI FACTS
# note range: 0-127 where 0 is C-1 and a step is a semitone
# pitch bend range -8191 to 8192, mapping to cents is unspecified
# channel range 0-15, pitch bend is applied to channels not notes

# output scale's first note is assumed to be C for convenience

import utils, weights, analytic, output
import tkinter as tk
from tkinter.filedialog import askopenfilename


def open_file():
    global midi_messages
    filename = askopenfilename(title='choose a midi score', initialdir='~')
    try:
        midi_messages = utils.preprocess(filename)
        label_info.config(text='file loaded')
    except Exception as e:
        label_info.config(text=e)

def run():
    try:
        scale = analytic.solve(weights.freq_weight(midi_messages), weights.interval_weight)
        output.scale_file('myscale', scale)
    except Exception as e:
        label_info.config(text=e)



root = tk.Tk()
root.title('InTune')
root.geometry('250x100')
root.resizable(False,False)

button_open_file = tk.Button(root, text='choose midi file', command=open_file)
button_run = tk.Button(root, text='run', command=run)
label_info = tk.Label()

button_open_file.pack()
button_run.pack()
label_info.pack()
root.mainloop()