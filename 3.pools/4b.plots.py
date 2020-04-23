#!/usr/bin/env python3
import math, numpy, pickle
from glbase3 import *
import matplotlib.pyplot as plot

'''

Round 1, For each domain, work out a dynamic threshold.

'''

oh = open('final_results.pickle', "rb")
domain = pickle.load(oh)
oh.close()

for dom_idx, dom in enumerate(domain):
    print(dom)
    # I need to work out the TP and FP for a range of thresholds:

    thresholds = numpy.arange(1, 100, 1) # powers of 10;

    tp = []
    fp = []

    #print([i for i in zip(domain[dom]['fp']['e'], domain[dom]['fp']['fp'])])

    for threshold in thresholds:
        #print(threshold)
        t = 10**-int(threshold)

        toadd = None
        for i, e in enumerate(domain[dom]['tp']['e']):
            if e > t:

                toadd = domain[dom]['tp']['tp'][i]
                #print(e, t, toadd)
                break
        if toadd:
            tp.append(toadd)
        else:
            try:
                tp.append(tp[-1])
            except IndexError:
                pass
                tp.append(-50)

        toadd = None
        for i, e in enumerate(domain[dom]['fp']['e']):
            if e > t:
                toadd = domain[dom]['fp']['fp'][i]
                #print(e, t, toadd)
                break
        if toadd:
            fp.append(toadd)
        else:
            try:
                fp.append(fp[-1])
            except IndexError:
                #fp.append(fp[0])
                fp.append(-50)

    # reset the -50's to max vals:
    newfp = []
    for f in fp:
        if f == -50:
            newfp.append(max(fp))
        else:
            newfp.append(f)
    fp = newfp

    newtp = []
    for f in tp:
        if f == -50:
            newtp.append(max(tp))
        else:
            newtp.append(f)
    tp = newtp

    #print([i for i in zip(tp, fp)])

    fig = plot.figure(figsize=[2,2])
    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0.2, bottom=0.2)
    ax.scatter(fp, tp)
    ax.plot(fp, tp)
    ax.set_title(dom, fontsize=6)
    ax.set_xlabel('True +', fontsize=6)
    ax.set_ylabel('False +', fontsize=6)
    plot.xticks(fontsize=6)
    plot.yticks(fontsize=6)
    #ax.set_xlim([0, 1])
    #ax.set_ylim([0, 1])
    #ax.set_yticks([0, 0.5, 1.0])
    fig.savefig('rocs/AUC_{0}.pdf'.format(dom))
    plot.close(fig)

    if dom_idx > 50:
        break
