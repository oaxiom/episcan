#!/usr/bin/env python3
import sys, os, glob, pickle
from glbase3 import *
sys.path.append('../')
import shared

[os.remove(f) for f in glob.glob('clusters/*.tsv')]
[os.remove(f) for f in glob.glob('clusters_genes/*.tsv')]

config.draw_mode = 'pdf'

e = glload('model_matrix-trained.glb')

#e = shared.remove_duplicates_by_e(e)

dom_anns = glload('../domains/annotation_table.glb')

num_clusters = 16

c = e.umap.cluster('KMeans', num_clusters=num_clusters)

e.umap.scatter(filename="scatter-final.png".format(num_clusters),
    label=False,
    size=[3,3],
    alpha=1.0,
    label_font_size=6)

#e.tsne.cluster_tree(filename='tsne-tree.pdf')

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

# get the genes identified by motifs in each cluster, must go to their best e-value domain only
# (i.e. each gene can only be added to a cluster once;
all_episcan = glload('../4.select/Hs.matches.glb')
print(all_episcan)

clus_genes = {c: [] for c in clus}

best_clusters = {}

print(motif_clus_membership)

for match in all_episcan:
    #if match['e'] < 1e-20: # Only get the really good match genes to stop weak overlaps to ogther clusters
    motif_cluster = motif_clus_membership[match['domain']]
    if match['ensg'] not in best_clusters:
        best_clusters[match['ensg']] = match
        best_clusters[match['ensg']]['bestE'] = 1e10

    if match['e'] < best_clusters[match['ensg']]['bestE']:
        best_clusters[match['ensg']]['best_clus'] = motif_cluster
        best_clusters[match['ensg']]['bestE'] = match['e']

for row in best_clusters:
    clus_genes[best_clusters[row]['best_clus']].append(best_clusters[row])

for motif_cluster in clus_genes:
    if not clus_genes[motif_cluster]:
        print("ERROR! {0} cluster is empty".format(motif_cluster))
        continue
    gl = genelist()
    gl.load_list(clus_genes[motif_cluster])
    gl = gl.removeDuplicates('ensg')

    gl.saveTSV('clusters_genes/clus_{0}.tsv'.format(motif_cluster), key_order=['ensg'])
    clus_genes[motif_cluster] = gl

data = [len(clus_genes[c]) for c in clus_genes]

print(data)

shared.radial_plot('radial.pdf',
    data=data,
    title='Homo Sapiens')
