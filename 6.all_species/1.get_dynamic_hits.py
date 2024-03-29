#!/usr/bin/env python3
import numpy, pickle, glob, sys, os
from glbase3 import *
import matplotlib.pyplot as plot

sys.path.append('../')
import shared

'''

Collect all the peptide hits using the models defined in stage 3.

'''

[os.remove(f) for f in glob.glob('model_hits/*.tsv')]
[os.remove(f) for f in glob.glob('model_hits_glbs/*.glb')]

final_results = {}
model_matrix = glload('../3.model/AUCtable.glb')
dynamicE = {d['domain']: float(d['e']) for d in model_matrix}

#########

for species in glob.glob('search_all/domtbl/*.tsv.gz'):
    try:
        hmmer_search = genelist(filename=species, format=format.hmmer_domtbl, gzip=True)
    except IndexError:
        print(f'ERROR! {species} IndexError')
        continue

    species = os.path.split(species)[1].replace('.tsv.gz', '')
    if species[0] == '_':
        continue

    matches = shared.get_dynamic_e(hmmer_search, dynamicE)

    if matches: # Sometimes it's empty;
        gl = genelist()
        gl.load_list(matches)
        gl = gl.removeDuplicates('unq_key') # unq_key = ensp-domain
        gl = gl.getColumns(['ensp', 'e', 'domain', 'len', 'dom_loc'])
        gl.sort('ensp')
        gl.saveTSV('model_hits/{0}.matches.tsv'.format(species), key_order=['ensp', 'domain', 'e'])
        gl.save('model_hits_glbs/{0}.matches.glb'.format(species))
