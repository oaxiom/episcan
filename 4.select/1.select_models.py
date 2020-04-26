#!/usr/bin/env python3
import numpy
from glbase3 import *

'''

For some set of criteria, select some models for FP/TP validation

'''

model_matrix = glload('../3.model/AUCtable.glb')

doms_to_keep = []

for model in model_matrix:
    print(model)

    if model['auc'] > 0.6:
        doms_to_keep.append(model)
        continue




# This will be the initial seed for the pools;
gl = genelist()
gl.load_list(doms_to_keep)
gl.saveTSV('passed_domains.tsv', key_order=['domain'])



