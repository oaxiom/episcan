#!/usr/bin/env python3
import numpy, pickle, sys
from glbase3 import *
import matplotlib.pyplot as plot
sys.path.append('../')
import shared

'''

Round 1, For each domain, work out a dynamic threshold for each motif, and discard motifs that are useless

'''

final_results = {}
model_matrix = glload('../3.model/AUCtable.glb')
dynamicE = {d['domain']: float(d['e']) for d in model_matrix}
epifactors_filtered = glload('../1.extract_epifactors_FASTA/mm_epifactors.all.glb').removeDuplicates('ensg')

#########

hmmer_search = genelist(filename='Mm.gencode.txt', format=format.hmmer_domtbl)

matches = shared.get_dynamic_e(hmmer_search, dynamicE)

# add wether it is in Epifactors DB, or not;

gl = genelist()
gl.load_list(matches)
gl.saveTSV('Mm.matches.tsv', key_order=['ensg', 'ensp', 'name'])
gl.save('Mm.matches.glb')

# Filtered result
episcan = set(gl.removeDuplicates('name')['name'])
epifactors = set(epifactors_filtered.removeDuplicates('name')['name'])

epifactors_only = epifactors.difference(episcan)
both = epifactors.intersection(episcan)
episcan_only = episcan.difference(epifactors)

print('Mm10: Episcan ( {0} ( {1} ) {2} ) Epifactors Filtered'.format(len(episcan_only), len(both), len(epifactors_only)))

with open('mm_result_filtered_epifactors_only.txt', 'wt') as oh:
    for name in sorted(epifactors_only):
        oh.write('{0}\n'.format(name))

with open('mm_result_filtered_both.txt', 'wt') as oh:
    for name in sorted(both):
        oh.write('{0}\n'.format(name))

with open('mm_result_filtered_episcan_only.txt', 'wt') as oh:
    for name in sorted(episcan_only):
        oh.write('{0}\n'.format(name))
