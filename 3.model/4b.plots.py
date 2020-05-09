#!/usr/bin/env python3
import math, numpy, pickle, sklearn, glob, sys, os
from glbase3 import *
import matplotlib.pyplot as plot

'''

Round 1, For each domain, work out a dynamic threshold.

'''

oh = open('final_results.pickle', "rb")
domain = pickle.load(oh)
oh.close()

auc_table = []
raw_table = []
auc_data = []

for dom_idx, dom in enumerate(domain):
    # I need to work out the TP and FP for a range of thresholds:

    thresholds = numpy.arange(1, 100, 1) # powers of 10;

    tp = []
    fp = []

    #print([i for i in zip(domain[dom]['fp']['e'], domain[dom]['fp']['fp'])])

    for threshold in thresholds:
        t = 10**-int(threshold)

        toadd = None
        for i, e in enumerate(domain[dom]['tp']['e']):
            if e >= t:
                toadd = i+1
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
            if e >= t:
                toadd = i+1
                break
        if toadd:
            fp.append(toadd)
        else:
            try:
                fp.append(fp[-1])
            except IndexError:
                #fp.append(fp[0])
                fp.append(-50)

    # In the last column, make sure all the TP and FP are added properly:
    # For example the TET domain all E-values are <1e-100, so it gets a score of 0
    tp.insert(0, len(domain[dom]['tp']['e']))
    fp.insert(0, len(domain[dom]['fp']['e']))

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
    #tp.append(0)
    #fp.append(0)

    #print(tp)
    #print(fp)

    # convert fp, tp to rates:
    tpr = numpy.array(tp) / (max(tp)+1)
    fpr = numpy.array(fp) / (max(fp)+1)

    optimal_idx = numpy.argmax(tpr - fpr)
    #print(tpr.shape, optimal_idx, tpr - fpr)
    optimal_threshold = optimal_idx
    if max(fp) >= 1:
        tpfp_ratio = max(tp) / max(fp)
    else:
        tpfp_ratio = 100

    auc = sklearn.metrics.auc(fpr, tpr)

    raw_table.append({'domain': dom, 'auc': auc, 'e': max([domain[dom]['tp_bestE']['max'], 1e-100]), 'TP/FP ratio': tpfp_ratio, 'TP': max(tp), 'FP': max(fp)})

    if max(tp) == 0: # usless;
        pass_criteria = 'max(tp) == 0'
        auc = 0.0
        elbowE = 1.0
        tpfp_ratio = 0
        tp = max(tp)
        fp = max(fp)
    elif max(fp) <= 0: # very good;
        pass_criteria = 'max(fp) == 0'
        auc = 1.0
        elbowE = min([0.1,
            max([domain[dom]['tp_bestE']['max']*100, 1e-100])
            ]) # super specific, so use the best matching E
        tp = max(tp)
        fp = max(fp)
    elif tpfp_ratio >= 3.0: # Probably also pretty good, but the E is a bit looser, set to the best E
        pass_criteria = 'TP/FP ratio'
        auc = 1.0
        elbowE = min([0.1, max([domain[dom]['tp_bestE']['max']*100, 1e-100])]) # i.e. smallest valid E or 1e-100
        tp = max(tp)
        fp = max(fp)
    else: # see if AUC thinks it's best:
        pass_criteria = 'AUC'
        elbowE = min([0.1,float('1e-{0}'.format(optimal_threshold))*100])
        # TP/FP ratio should be the numebr at that threshold!
        print(tp, fp)
        tp = tp[optimal_threshold]
        fp = fp[optimal_threshold]
        tpfp_ratio = tp / fp

    auc_data.append({'fpr': fpr, 'tpr': tpr})
    auc_table.append({'domain': dom, 'auc': auc, 'e': elbowE, 'TP/FP ratio': tpfp_ratio, 'TP': tp, 'FP': fp, 'pass_criteria': pass_criteria})
    title = '{0} AUC={1:.2f} e={2}\nTP={3} FP={4} TP/FP={5:.2f} pass_criteria={6}'.format(dom, auc, elbowE, tp, fp, tpfp_ratio, pass_criteria)
    print(title.replace('\n', ' '))

aucgl = genelist()
aucgl.load_list(auc_table)
aucgl.sort('auc')
aucgl.reverse()
aucgl.saveTSV('AUCtable.tsv')
aucgl.save('AUCtable.glb')

aucgl = genelist()
aucgl.load_list(raw_table)
aucgl.sort('auc')
aucgl.reverse()
aucgl.saveTSV('AUCtable_raw.tsv')
aucgl.save('AUCtable_raw.glb')

print('Drawing...')

[os.remove(f) for f in glob.glob('rocs/*.pdf')]

for d, t in zip(auc_data, auc_table):
    title = '{0} AUC={1:.2f} e={2}\nTP={3} FP={4} TP/FP={5:.2f}'.format(t['domain'], t['auc'], t['e'], t['TP'], t['FP'], t['TP/FP ratio'])
    fig = plot.figure(figsize=[2,2])
    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0.2, bottom=0.2)
    ax.scatter(d['fpr'], d['tpr'], s=6)
    ax.plot(d['fpr'], d['tpr'])
    ax.set_title(title, fontsize=6)
    ax.set_xlabel('False + & False -', fontsize=6)
    ax.set_ylabel('True +', fontsize=6)
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    plot.xticks(fontsize=6)
    plot.yticks(fontsize=6)
    if tpfp_ratio != 0.0:
        ax.axvline((-math.log10(t['e'])/100), c='steelblue', ls=':', lw=1.0)
        ax.axvline(optimal_idx/100, c='grey', ls=':', lw=0.5)
    fig.savefig('rocs/AUC_{0}.pdf'.format(t['domain'].replace('/', '-')))
    plot.close(fig)


