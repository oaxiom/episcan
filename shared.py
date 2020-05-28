
import numpy as np
import matplotlib.pyplot as plot

def get_division_cols(gl):
    row_cols = []
    for i in gl:
        if i['division'] == 'Fungi':
            row_cols.append('purple')
        elif i['division'] == 'Vertebrates':
            row_cols.append('red')
        elif i['division'] == 'Metazoa':
            row_cols.append('orange')
        elif i['division'] == 'Plants':
            row_cols.append('green')
        elif i['division'] == 'Protists':
            row_cols.append('blue')
        else:
            row_cols.append('grey')
            print(i['division'], 'Not found')
    return row_cols

def radial_plot(filename, data, title):
    fig = plot.figure(figsize=(6,6))
    #fig.subplots_adjust(0.02, 0.02, 0.97, 0.97, wspace=0.1, hspace=0.1)

    ax = fig.add_subplot(111, polar=True)

    erad = 2*np.pi / (len(data)+1) # each segment gets 0.69813170079773 (or thereabouts) rads
    eradh = erad / 2.0
    eradq = eradh / 2.0
    theta = np.arange(0.0, 2*np.pi, 2*np.pi/len(data))
    width = (np.pi/4)*len(data) # in rads?
    width = 0.5

    ax.bar(theta+(0.6981317/2), data, width=erad, bottom=0.0, alpha=0.8, color='red')

    ax.set_title(title)
    ax.set_xticks(theta)
    ax.set_xticklabels("")
    #ax.set_yticklabels("") # For hte svg

    #l = ax.get_rlim()
    #ax.set_rticks([0.5, 1, 1.5, 2])

    l = ax.get_ylim()
    #print k, ["%s%%" % i for i in range(l[0], l[1]+5, l[1]//len(axes[k].get_yticklabels()))]
    #print [str(t) for t in axes[k].get_yticklabels()]
    [t.set_fontsize(6) for t in ax.get_yticklabels()]
    #print ["%s%%" % (i*10, ) for i, t in enumerate(axes[k].get_yticklabels())]
    #print [t.get_text() for t in axes[k].get_yticklabels()]
    ylabs = ["%s%%" % str(i) for i in range(int(l[0]), int(l[1])+5, int(l[1]//len(ax.get_yticklabels())))][1:]
    #axes[k].set_yticklabels(ylabs)

    fig.savefig(filename)

if __name__ == "__main__":
    data = [33, 83, 92, 94, 12, 66, 69, 73, 56, 87, 74, 42, 104, 34, 19, 57, 38, 67, 2, 42, 122, 113, 53, 67, 23, 128, 77, 16, 25, 86, 26, 109]

    radial_plot('Homo_sapiens.pdf',
        data=data,
        title='Homo Sapiens')
