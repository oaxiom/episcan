#!/usr/bin/env python3
import numpy
from glbase3 import *

'''

For some set of criteria, select some models for FP/TP validation

'''

model_matrix = glload('../3.model/AUCtable.glb')
dom_anns = glload('../domains/annotation_table.glb')
dom_anns = dom_anns.renameKey('name', 'domain')

doms_to_keep = []

passed_by = {}

for model in model_matrix:
    # ALL selection is in ../3.select/5.final_scores.py
    doms_to_keep.append(model)
    if model['pass_criteria'] not in passed_by:
        passed_by[model['pass_criteria']] =0
    passed_by[model['pass_criteria']] += 1

print('Kept {0} domains'.format(len(doms_to_keep)))

# This will be the initial seed for the pools;
gl = genelist()
gl.load_list(doms_to_keep)

gl = gl.map(genelist=dom_anns, key='domain')

gl.saveTSV('passed_domains.tsv', key_order=['domain'])
gl.save('passed_domains.glb')

print()
for k in passed_by:
    print('{0}\t: {1}'.format(k, passed_by[k]))

