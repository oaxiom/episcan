#!/usr/bin/env python3
import sys, re, os, math
from glbase3 import *

# Generates a matrix of genes (rows) and models, where a 0 and 1 is used to indicate
# if the HMM is used or not used.
# This can then be used to build a tree, which we can simplify by merging branches to
# arrive at a summary of the epigenetic system;

all_episcan = glload('../4.select/Hs.matches.glb')

# Get the list of domains in use
doms = set([])
for match in all_episcan:
    name = match['domain']
    doms.add(name)

doms = list(doms)
doms.sort()
print('Found {0:,} unique domains'.format(len(doms)))

# Build initial table:
tab = {}
ensp_lookup = {}
for ensp, name in zip(all_episcan['ensp'], all_episcan['name']):
    tab[(ensp, name)] = {k: 0 for k in doms}
    ensp_lookup[ensp] = name

biggest_e = 0

for line in all_episcan:
    name = line['domain']
    ensp = line['ensp']

    if line['e'] == 0:
        e = 300
    else:
        e = -math.log10(line['e'])
    if e > biggest_e:
        biggest_e = e
        print('New Biggest E', biggest_e)

    #tab[(ensp, ensp_lookup[ensp])][name] = max([tab[(ensp, ensp_lookup[ensp])][name], e, 10])
    tab[(ensp, ensp_lookup[ensp])][name] = 1 # max([tab[(ensp, ensp_lookup[ensp])][name], e, 10])

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

e = e.filter_low_expressed(0.9, 1)

e.save('model_matrix.glb')
