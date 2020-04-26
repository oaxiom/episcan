#!/usr/bin/env python3
import numpy, pickle
from glbase3 import *
import matplotlib.pyplot as plot

'''

Round 1, For each domain, work out a dynamic threshold for each motif, and discard motifs that are useless

'''

final_results = {}
model_matrix = glload('../3.model/AUCtable.glb')
dynamicE = {d['domain']: d['e'] for d in model_matrix}
epifactors = glload('../1.extract_epifactors_FASTA/hs_epifactors.all.glb')#.removeDuplicates('ensg')
print(epifactors)

#########

tp = genelist(filename='Hs.gencode.txt', format=format.hmmer_domtbl)

#########
matches = []
for hit in tp:
    domain = hit['dom_name']
    print(tp)

    e = float(hit['e'])
    if e < dynamicE[domain]:
        e = 1e-100
    matches.append(hit)

# add wether it is in Epifactors DB, or not;

gl = genelist()
gl.load_list(matches)
gl.saveTSV('Hs.matches.tsv')


