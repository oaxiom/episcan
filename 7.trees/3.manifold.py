#!/usr/bin/env python3
import sys, re, os
from glbase3 import *

e = glload('model_matrix.glb')
#e.log(2,.1)
#print(e.getConditionNames())

all_ensp = len(e)

config.draw_mode = 'pdf'

pca = e.get_pca(feature_key_name='name', whiten=False)
pca.train(100)

cols = "grey"

pca.explained_variance(filename="loading.png")
#pca.scatter3d(filename="scatter123.png", x=1, y=2, z=3, depthshade=True, label=False, spot_cols=cols)
pca.scatter(filename="scatter12.png", x=1, y=2, label=False, spot_cols=cols, size=[3,3], label_font_size=6)

e.tsne.configure(whiten=False, random_state=123456)
e.tsne.train('all_matrix', perplexity=50)
e.tsne.scatter(filename="tsne-scatter.png", label=False, spot_cols=cols, size=[3,3], label_font_size=6)
'''
e.mds.configure(whiten=False, random_state=123456)
e.mds.train(10)
e.mds.scatter(filename="mds-scatter.png", label=False, spot_cols=cols, size=[3,3], label_font_size=6)
'''
e.umap.configure(whiten=False, random_state=123456)
e.umap.train(10, n_neighbors=20)
e.umap.scatter(filename="umap-scatter.png", label=False, spot_cols=cols, size=[3,3], label_font_size=6)


e.save('model_matrix-trained.glb')
