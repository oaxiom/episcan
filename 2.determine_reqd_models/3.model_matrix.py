#!/usr/bin/env python3
import sys, re, os
from glbase3 import *

# Generates a matrix of genes (rows) and models, where a 0 and 1 is used to indicate
# if the HMM is used or not used.

all_epifactors = glload('../1.extract_epifactors_FASTA/hs_epifactors.all.glb')
pfam = genelist(filename='pfam.txt', format=format.hmmer_domtbl)
print(pfam)
# Get the list of domains in use
doms = []
for line in pfam:
    hmm = line['dom_acc']
    name = line['dom_name']

    if '{0}:{1}'.format(name, hmm) not in doms:
        doms.append('{0}:{1}'.format(name, hmm))

doms = list(set(doms))
doms.sort()
print('Found {0:,} unique domains'.format(len(doms)))

# Build initial table:
tab = {}
ensp_lookup = {}
for ensp, name in zip(all_epifactors['ensp'], all_epifactors['name']):
    tab[(ensp, name)] = {k: 0 for k in doms}
    ensp_lookup[ensp] = name

for line in pfam:
    hmm = line['dom_acc']
    name = line['dom_name']
    ensp = line['peptide']

    tab[(ensp, ensp_lookup[ensp])]['{0}:{1}'.format(name, hmm)] = 1

oh = open('model_matrix_hits.tsv', 'w')
oh.write('{0}\n'.format('\t'.join(['ensp', 'name'] + doms)))
gltab = []
for item in tab:
    row = [tab[item][d] for d in doms] # enforce order just in case
    oh.write('{0}\n'.format('\t'.join(list(item) + [str(i) for i in row])))
    gltab.append({'name': item[1], 'ensp': item[0], 'conditions': [i for i in row]})
oh.close()

# heatmap
e = expression(loadable_list=gltab, cond_names=doms)
e.save('model_matrix.glb')

filte = e.filter_low_expressed(0.9,1)
detected = filte.removeDuplicates('name')
print(detected.getColumns(['name'], strip_expn=True))
print(e.getColumns(['name'], strip_expn=True))
try:
    os.remove('undetected_by_hmmer.tsv')
except FileNotFoundError:
    pass
undetected = detected.map(genelist=e, key='name', logic='notright')
if undetected:
    undetected = undetected.getColumns(['ensp', 'name'], strip_expn=True)
    undetected = undetected.removeDuplicates('name')
    undetected.sort('name')
    undetected.saveTSV('undetected_by_hmmer.tsv')

    if len(undetected) < len(detected):
        print('Warning! Undetected={0} < {1}=AllNames, reduce your Evalue?'.format(len(undetected), len(detected)))

filte.getColumns(['ensp', 'name'], strip_expn=True).saveTSV('detected_by_hmmer.tsv')

all_ensp = len(e)

config.draw_mode = 'pdf'
filte.heatmap('all_models.pdf', border=True, imshow=True,
    col_cluster=True,
    heat_wid=0.75, optimal_ordering=True,
    size=[12,12])
