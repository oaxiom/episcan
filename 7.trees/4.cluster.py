#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *

[os.remove(f) for f in glob.glob('clusters/*.tsv')]

config.draw_mode = 'pdf'

e = glload('model_matrix-trained.glb')
dom_anns = glload('../domains/annotation_table.glb')

num_clusters = 20

c = e.tsne.cluster('KMeans', num_clusters=num_clusters)

e.tsne.scatter(filename="tsne-scatter-cluster.png",
    label=False,
    size=[3,3],
    label_font_size=6)

print(len(c[1]))

clus = {i: [] for i in range(num_clusters)}
for k, c in zip(e.getConditionNames(), c[1]):
    clus[c].append(k)

for c in clus:
    gl = genelist()
    gl.load_list([{'name': i} for i in clus[c]])

    gl = gl.map(genelist=dom_anns, key='name')

    gl.saveTSV('clusters/clus_{0}.tsv'.format(c))
