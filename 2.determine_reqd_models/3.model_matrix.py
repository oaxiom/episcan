#!/usr/bin/env python3
import sys, re
from glbase3 import *

# Generates a matrix of genes (rows) and models, where a 0 and 1 is used to indicate
# if the HMM is used or not used.

all_epifactors = glload('../1.extract_epifactors_FASTA/hs_epifactors.all.glb')
pfam = genelist(filename='pfam.txt', format=format.hmmer_tbl)

# Get the list of domains in use
doms = []
for line in pfam:
    hmm = line['score'] # all in the wrong columns
    name = line['dom_acc']

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
    hmm = line['score'] # all in the wrong columns
    name = line['dom_acc']
    ensp = line['peptide']
    
    tab[(ensp, ensp_lookup[ensp])]['{0}:{1}'.format(name, hmm)] = 1
    
oh = open('model_matrix_hits.tsv', 'w')
oh.write('{0}\n'.format('\t'.join(['ensp', 'name'] + doms)))
for item in tab:
    row = [tab[item][d] for d in doms] # enforce order just in case
    oh.write('{0}\n'.format('\t'.join(list(item) + [str(i) for i in row])))
oh.close()