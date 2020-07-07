#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *

[os.remove(f) for f in glob.glob('clusters/*.tsv')]

config.draw_mode = 'pdf'

e = glload('model_matrix-trained.glb')
dom_anns = glload('../domains/annotation_table.glb')

for num_clusters in range(2, 50):
    c = e.umap.cluster('KMeans', num_clusters=num_clusters)

    e.umap.scatter(filename="clusters_pdf/scatter-cluster-{0}.png".format(num_clusters),
        label=False,
        size=[3,3],
        label_font_size=6
        )

