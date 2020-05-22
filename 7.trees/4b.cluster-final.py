#!/usr/bin/env python3
import sys, os, glob, pickle
from glbase3 import *

sys.path.append('../')
import shared

[os.remove(f) for f in glob.glob('clusters/*.tsv')]

config.draw_mode = 'pdf'

e = glload('model_matrix-trained.glb')
dom_anns = glload('../domains/annotation_table.glb')

num_clusters = 32

c = e.tsne.cluster('AgglomerativeClustering', num_clusters=num_clusters)

e.tsne.scatter(filename="tsne-scatter-final.png".format(num_clusters),
    label=False,
    size=[3,3],
    alpha=1.0,
    label_font_size=6)

e.tsne.cluster_tree(filename='tsne-tree.pdf')

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

oh = open('cluster-domains.pickle', "wb")
pickle.dump(clus, oh, -1)
oh.close()

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
    clus_genes[motif_cluster] = gl

data = [len(clus_genes[c]) for c in clus_genes]

print(data)

shared.radial_plot('radial.pdf',
    data=data,
    title='Homo Sapiens')
