#!/usr/bin/env python3
import sys, re, os
from glbase3 import *

e = glload('model_matrix.glb')
#print(e.getConditionNames())

all_ensp = len(e)

config.draw_mode = 'pdf'

pca = e.get_pca(feature_key_name='name', whiten=True)
pca.train(20)

cols = "grey"

pca.explained_variance(filename="loading.png")
#pca.scatter3d(filename="scatter123.png", x=1, y=2, z=3, depthshade=True, label=False, spot_cols=cols)
#pca.scatter(filename="scatter12.png", x=1, y=2, label=True, spot_cols=cols, size=[3,3], label_font_size=6)

e.tsne.configure(whiten=False, random_state=11142)
e.tsne.train(3, perplexity=20)
e.tsne.scatter(filename="tsne-scatter.png", label=False, spot_cols=cols, size=[3,3], label_font_size=6)

e.save('model_matrix-trained.glb')
