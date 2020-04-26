#!/usr/bin/env python3
import math, numpy, pickle, sklearn
from glbase3 import *
import matplotlib.pyplot as plot

'''

Round 1, For each domain, work out a dynamic threshold.

'''

oh = open('final_results.pickle', "rb")
domain = pickle.load(oh)
oh.close()

auc_table = []

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
            newfp.append(max(0, max(fp)))
        else:
            newfp.append(f)
    fp = newfp

    newtp = []
    for f in tp:
        if f == -50:
            newtp.append(max(0, max(tp)))
        else:
            newtp.append(f)
    tp = newtp

    #tp.insert(0, max(tp)+1) # curve needs to be filled in for AUC score
    #fp.insert(0, max(fp)+1)
    tp.append(0)
    fp.append(0)

    #print(tp)
    #print(fp)

    # convert fp, tp to rates:
    tpr = numpy.array(tp) / (max(tp)+1)
    fpr = numpy.array(fp) / (max(fp)+1)

    optimal_idx = numpy.argmax(tpr - fpr)
    optimal_threshold = thresholds[optimal_idx-1]

    if max(tp) == 0: # usless;
        auc = 0.0
        elbow = 0.0
        elbowE = 1.0
        tpfp_ratio = 0
    elif max(fp) == 0: # very good;
        auc = 1.0
        elbow = 1.0
        elbowE = 1e-100 # super specific.
        tpfp_ratio = 100 # actually infinite?
    else:
        auc = sklearn.metrics.auc(fpr, tpr)
        elbow = 1
        elbowE = 1
        tpfp_ratio = max(tp) / max(fp)

    auc_table.append({'domain': dom, 'auc': auc, 'elbow': elbow, 'e': elbowE, 'TP/FP ratio': tpfp_ratio})

    fig = plot.figure(figsize=[2,2])
    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0.2, bottom=0.2)
    ax.scatter(fpr, tpr, s=6)
    ax.plot(fpr, tpr)
    ax.set_title('{0} AUC={1:.2f} e={2}\nTP={3} FP={4}'.format(dom, auc, optimal_threshold, max(tp), max(fp)), fontsize=6)
    ax.set_xlabel('False +', fontsize=6)
    ax.set_ylabel('True +', fontsize=6)
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    plot.xticks(fontsize=6)
    plot.yticks(fontsize=6)
    ax.axvline(optimal_idx/100, c='grey', ls=':')
    fig.savefig('rocs/AUC_{0}.pdf'.format(dom))
    plot.close(fig)

aucgl = genelist()
aucgl.load_list(auc_table)
aucgl.sort('auc')
aucgl.reverse()
aucgl.saveTSV('AUCtable.tsv')
aucgl.save('AUCtable.glb')
