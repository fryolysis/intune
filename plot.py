import matplotlib.pyplot as plt


def plot(tunedscore, title):

    data = [[] for _ in range(12)]
    time = [[] for _ in range(12)]
    for n in tunedscore:
        val = (n.solution+50)%1200 - 50
        data[n.semitones%12].append(val)
        time[n.semitones%12].append(n.start)

    # plot
    fig, ax = plt.subplots()
    for gr_t,gr in zip(time, data):
        ax.plot(gr_t, gr, '.', markersize=2)
    
    ax.set(yticks=range(0,1250,100), xlabel='Time(s)', ylabel='Cents', title=title)
    plt.grid(axis='y')
    plt.show()