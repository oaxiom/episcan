#!/usr/bin/env python3
import numpy, pickle
from glbase3 import *
import matplotlib.pyplot as plot

'''

Round 1, For each domain, work out a dynamic threshold for each motif, and discard motifs that are useless

'''

final_results = {}

#########
print('Doing T+')
tp = genelist(filename='round2.epifactors.TP.txt', format=format.hmmer_domtbl)
true_positives = {} # per domain;
for hit in tp:
    domain = hit['dom_name']

    if domain not in true_positives:
        true_positives[domain] = []
    e = float(hit['e'])
    if e < 1e-100:
        e = 1e-100
    true_positives[domain].append(e)

# Now we have the set of e, we have the maximum possible TP (len(true_positives))

for domain in true_positives:
    # Add the TP for each threshold
    num_hits = len(true_positives[domain])
    for i, e in enumerate(sorted(true_positives[domain])):
        if domain not in final_results:
            final_results[domain] = {
                'tp': {'e': [], 'tp': []},
                'fp': {'e': [], 'fp': []}
                }

        final_results[domain]['tp']['e'].append(e)
        final_results[domain]['tp']['tp'].append(i)
    # 1.10.10.10/FF/170430
    final_results[domain]['tp_bestE'] = {
        'min': min(final_results[domain]['tp']['e']),
        'max': max(final_results[domain]['tp']['e'])
        }
    print(domain, final_results[domain]['tp_bestE'])

#for d in final_results:
#    print(d)
#    print([i for i in zip(final_results[d]['tp']['e'], final_results[d]['tp']['tp'])])

#########
print('Doing F+')
fp = genelist(filename='round2_gencode_FP.txt', format=format.hmmer_domtbl)
false_positives = {} # per domain;
for hit in fp:
    domain = hit['dom_name']

    if domain not in false_positives:
        false_positives[domain] = []
    e = float(hit['e'])
    if e < 1e-100:
        e = 1e-100
    false_positives[domain].append(e)

# Now we have the set of e, we have the maximum possible TP (len(false_positives))

for domain in false_positives:
    # Add the TP for each threshold
    num_hits = len(false_positives[domain])
    for i, e in enumerate(sorted(false_positives[domain])):
        final_results[domain]['fp']['e'].append(e)
        final_results[domain]['fp']['fp'].append(i)

    final_results[domain]['fp_bestE'] = {'min': min(final_results[domain]['tp']['e']), 'max': max(final_results[domain]['tp']['e'])}

#for d in final_results:
#    print(d)
#    print([i for i in zip(final_results[d]['fp']['e'], final_results[d]['fp']['fp'])])

oh = open('final_results.pickle', "wb")
pickle.dump(final_results, oh, -1)
oh.close()

