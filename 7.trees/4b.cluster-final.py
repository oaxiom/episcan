#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *

sys.path.append('../')
import shared

[os.remove(f) for f in glob.glob('clusters/*.tsv')]

config.draw_mode = 'pdf'

e = glload('model_matrix-trained.glb')
dom_anns = glload('../domains/annotation_table.glb')

num_clusters = 16

c = e.tsne.cluster('KMeans', num_clusters=num_clusters)

clus = {i: [] for i in range(num_clusters)}
motif_clus_membership = {}
for k, c in zip(e.getConditionNames(), c[1]):
    clus[c].append(k)
    motif_clus_membership[k] = c

for c in clus:
    gl = genelist()
    gl.load_list([{'name': i} for i in clus[c]])

    gl = gl.map(genelist=dom_anns, key='name')

    gl.saveTSV('clusters/clus_{0}.tsv'.format(c))

# get the genes identified by motifs in each cluster
all_episcan = glload('../4.select/Hs.matches.glb')
print(all_episcan)

clus_genes = {c: [] for c in clus}

for match in all_episcan:
    motif_cluster = motif_clus_membership[match['domain']]
    clus_genes[motif_cluster].append({'ensg': match['ensg'], 'name': match['name']})

for motif_cluster in clus_genes:
    gl = genelist()
    gl.load_list(clus_genes[motif_cluster])
    gl = gl.removeDuplicates('ensg')

    gl.saveTSV('clusters_genes/clus_{0}.tsv'.format(motif_cluster))


