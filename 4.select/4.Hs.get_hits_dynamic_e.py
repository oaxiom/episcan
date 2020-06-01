#!/usr/bin/env python3
import sys, os, numpy, pickle
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
epifactors_filtered = glload('../1.extract_epifactors_FASTA/hs_epifactors.all.glb').removeDuplicates('ensg')
epifactors_unfiltered = glload('../1.extract_epifactors_FASTA/hs_epifactors.unfiltered.glb').removeDuplicates('ensg')

#########

hmmer_search = genelist(filename='Hs.gencode.txt', format=format.hmmer_domtbl)

matches = matches = shared.get_dynamic_e(hmmer_search, dynamicE)

# TODO: add wether it is in Epifactors DB, or not;

gl = genelist()
gl.load_list(matches)
gl.saveTSV('Hs.matches.tsv', key_order=['ensg', 'ensp', 'name'])
gl.save('Hs.matches.glb')

print(gl)

# Unfiltered result:

episcan = set(gl.removeDuplicates('name')['name'])
epifactors = set(epifactors_unfiltered.removeDuplicates('name')['name'])

epifactors_only = epifactors.difference(episcan)
both = epifactors.intersection(episcan)
episcan_only = episcan.difference(epifactors)

print('Episcan ( {0} ( {1} ) {2} ) Epifactors Unfiltered'.format(len(episcan_only), len(both), len(epifactors_only)))

with open('result_unfiltered_epifactors_only.txt', 'wt') as oh:
    for name in sorted(epifactors_only):
        oh.write('{0}\n'.format(name))

with open('result_unfiltered_both.txt', 'wt') as oh:
    for name in sorted(both):
        oh.write('{0}\n'.format(name))

with open('result_unfiltered_episcan_only.txt', 'wt') as oh:
    for name in sorted(episcan_only):
        oh.write('{0}\n'.format(name))

# Filtered result
episcan = set(gl.removeDuplicates('name')['name'])
epifactors = set(epifactors_filtered.removeDuplicates('name')['name'])

epifactors_only = epifactors.difference(episcan)
both = epifactors.intersection(episcan)
episcan_only = episcan.difference(epifactors)

print('Episcan ( {0} ( {1} ) {2} ) Epifactors Filtered'.format(len(episcan_only), len(both), len(epifactors_only)))

with open('result_filtered_epifactors_only.txt', 'wt') as oh:
    for name in sorted(epifactors_only):
        oh.write('{0}\n'.format(name))

with open('result_filtered_both.txt', 'wt') as oh:
    for name in sorted(both):
        oh.write('{0}\n'.format(name))

with open('result_filtered_episcan_only.txt', 'wt') as oh:
    for name in sorted(episcan_only):
        oh.write('{0}\n'.format(name))
