#!/usr/bin/env python3
import sys, re, os
from glbase3 import *

e = glload('model_matrix.glb')
#print(e.getConditionNames())

all_ensp = len(e)

config.draw_mode = 'pdf'

e.tree(filename='all_tree.pdf', label_size=4, figsize=[6,12])

e.heatmap('all_models.pdf', border=True, imshow=True,
    col_cluster=True,
    heat_wid=0.75, optimal_ordering=True,
    size=[12,12])
