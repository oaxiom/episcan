#!/usr/bin/env python3
import sys, re, os
import matplotlib.cm as cmap
from glbase3 import *

e = glload('model_matrix.glb')
e.log(2, .1)
#print(e.getConditionNames())

all_ensp = len(e)

config.draw_mode = 'pdf'

e.tree(filename='all_tree.pdf', label_size=4, figsize=[6,12])

e.heatmap('all_models.pdf', border=True, imshow=True,
    col_cluster=True,
    cmap=cmap.plasma_r,
    #bracket=[0,200],
    heat_wid=0.75,
    col_font_size=3,
    row_font_size=3,
    optimal_ordering=True,
    size=[12,12])
