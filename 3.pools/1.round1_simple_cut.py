#!/usr/bin/env python3
from glbase3 import *

'''

Round 1, we cut domains that are redundant with other doamins.

Basically, if they fidn the same genes, we trim them from the list

'''

pfam = genelist(filename='../2.determine_reqd_models/pfam.txt', format=format.hmmer_tbl)

doms = {}

for dom in pfam:
    if dom['dom_acc'] not in doms:
        doms[dom['dom_acc']] = []
    doms[dom['dom_acc']].append(dom['peptide'])

pair_doms = []
for i1, dom1 in enumerate(doms):
    for i2, dom2 in enumerate(doms):
        if i1 > i2:
            if len(dom1) == len(dom2):
                # Check all the same
                if False not in [i1 == i2 for i1, i2 in zip(doms[dom1], doms[dom2])]:
                    pair_doms.append(dom2)
                    pair_doms.append(dom1) 
                    # Work out the sum of scores...


print(pair_doms)                
    

