#!/usr/bin/env python3
import numpy
from glbase3 import *

'''

Round 1, we cut domains that are redundant with other doamins.

Basically, if they find the exact same proteins, we can trim them from the list

'''

model_matrix = glload('../2.determine_reqd_models/model_matrix.glb')
all_models = model_matrix.getConditionNames()

# Now I need to work out the most senstiive one, and keep that:
pfam = genelist(filename='../2.determine_reqd_models/pfam.txt', format=format.hmmer_domtbl)
print(pfam)
scores = {}

for model in all_models:
    this_model = model_matrix.getDataForCondition(model)
    s = sum(this_model)
    if s not in scores:
        scores[s] = []
    scores[s].append((model, this_model))

doms_to_keep = []

# test those with a matching score
todo = len(scores)
for idx, score in enumerate(scores):
    if len(scores[score]) == 1:
        doms_to_keep.append({'name': scores[score][0][0], 'frequency': score})
        continue

    dupes = set([])
    for i1, m1 in enumerate(scores[score]):
        for i2, m2 in enumerate(scores[score]):
            if i1 < i2:
                if numpy.array_equal(m1[1], m2[1]):
                    dupes.add(m1[0])
                    dupes.add(m2[0])

    if dupes:
        dupes = set(dupes)
        #print('{0} are dupes'.format('\t'.join(list(dupes))))

        dupe_es = {d: 0.0 for d in dupes}
        # get the sum of e-values for each HMM:
        for i in pfam:
            hmm_name = '{0}:{1}'.format(i['dom_name'], i['dom_acc'])
            if hmm_name in dupe_es:
                dupe_es[hmm_name] += float(i['e'])

        best_e = min(dupe_es, key=dupe_es.get)
        doms_to_keep.append({'name': best_e, 'frequency': score})

    else: # need to add all the PWMs:
        for m in scores[score]:
            doms_to_keep.append({'name': m[0], 'frequency': score})

    if idx % 10 == 0:
        print('Done {0}/{1}'.format(idx, todo))

print(doms_to_keep)

# This will be the initial seed for the pools;
gl = genelist()
gl.load_list(doms_to_keep)
gl.sort('frequency')
gl.reverse()
gl.save('domains_round1.glb')
gl.saveTSV('domains_round1.txt', key_order=['name'])



