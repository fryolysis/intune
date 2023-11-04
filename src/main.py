# MIDI FACTS
# note range: 0-127 where 0 is C-1 and a step is a semitone
# pitch bend range -8191 to 8192, mapping to cents is unspecified
# channel range 0-15, pitch bend is applied to channels not notes

# output scale's first note is assumed to be C for convenience

from intune.src import analytic, output, utils, weights
import tkinter as tk
import tkinter.filedialog as fd

button_color = '#7ec4b0'

def open_file():
    global midi_messages
    filename = fd.askopenfilename(title='choose a midi score', initialdir='~')
    try:
        midi_messages = utils.preprocess(filename)
        label_info.config(text='file loaded')
    except Exception as e:
        label_info.config(text=f'Error:{e}')

def run():
    global scale
    try:
        scale = analytic.solve(weights.window_weight(midi_messages), weights.interval_weight)
        print(scale)
        label_scale.config(text=output.scale_label(scale))
        label_info.config(text='done')
    except Exception as e:
        print(e.with_traceback())
        label_info.config(text=f'Error:{e}')

def export_scale():
    fname = fd.asksaveasfilename(title='save file as', initialdir='~', defaultextension='.scl')
    try:
        output.scale_file(fname, scale)
        label_info.config(text=f'saved as {fname}')
    except Exception as e:
        label_info.config(text=f'Error:{e}')

root = tk.Tk()
root.title('InTune')
root.geometry('300x250')
root.config(bg='#d6d196')


control_frame = tk.Frame(root)
display_frame = tk.LabelFrame()

button_open_file = tk.Button(control_frame, text='choose midi file', command=open_file, bg=button_color)
button_run = tk.Button(control_frame, text='run', command=run, bg=button_color)
button_export_scale = tk.Button(control_frame, text='export scale', command=export_scale, bg=button_color)
label_info = tk.Label(display_frame, wraplength=100)
label_scale = tk.Label(display_frame, wraplength=100)


control_frame.pack(side='left', anchor='s')
display_frame.pack(side='right', anchor='s')

label_info.pack(side='bottom', anchor='s')
label_scale.pack(side='top')
for wg in control_frame.winfo_children():
    wg.pack(anchor='w', fill='x')

root.mainloop()