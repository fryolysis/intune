import matplotlib.pyplot as plt
from params import WINSIZE
from utils import Note
import numpy as np
from solve import kappa, ZERO_WEIGHT

def trick(x):
    return (x+50)%1200 - 50

def plot(tunedscore, title):

    data = [[] for _ in range(12)]
    time = [[] for _ in range(12)]
    for n in tunedscore:
        val = trick(n.solution)
        data[n.semitones%12].append(val)
        time[n.semitones%12].append(n.start)

    # plot
    _, ax = plt.subplots()
    for gr_t,gr in zip(time, data):
        ax.plot(gr_t, gr, '.', markersize=2)
    
    ax.set(yticks=range(0,1250,100), xlabel='Time(s)', ylabel='Cents', title=title)
    plt.grid(axis='y')
    plt.show()


def error_report(score: list[Note]):
    intervals = [[] for _ in range(12)]
    for i in range(len(score)):
        for j in range(-WINSIZE, WINSIZE+1):
            if j==0 or i+j < 0 or i+j >= len(score) or kappa(score[i], score[i+j]) <= 2*ZERO_WEIGHT:
                continue
            interval_class = abs(score[i].semitones - score[i+j].semitones)%12
            cur_interval = trick( abs(score[i].solution - score[i+j].solution) )
            intervals[interval_class].append(cur_interval)
    print('Average and std. dev. of sizes of important interval classes:')
    for i in intervals:
        if i:
            a = np.array(i)
            print(round(np.mean(a),1), '\t\t', round(np.std(a),1))

    plt.hist(intervals[0], label='Unison/Octave', histtype='step')
    plt.hist(intervals[5], label='Fourth', histtype='step')
    plt.hist(intervals[4], label='Third', histtype='step')
    plt.hist(intervals[7], label='Fifth', histtype='step')