#!/usr/bin/env python3
import numpy, pickle, glob
from glbase3 import *
import matplotlib.pyplot as plot

'''

Collect all the peptide hits using the models defined in stage 3.

'''

final_results = {}
model_matrix = glload('../3.model/AUCtable.glb')
dynamicE = {d['domain']: float(d['e']) for d in model_matrix}

#########

for species in glob.glob('cluster/episcan_species/searches/*/domtbl_out.tsv.gz'):
    hmmer_search = genelist(filename=species, format=format.hmmer_domtbl, gzip=True)

    matches = []
    for hit in hmmer_search:
        domain = hit['dom_name']

        e = float(hit['e'])

        #print(hit, e, dynamicE[domain], e < dynamicE[domain])
        if e < dynamicE[domain]:
            #print(hit)
            matches.append({'ensp': hit['peptide'],
                'e': e,
                'domain': hit['dom_name'],
                'unq_key': '{0}-{1}'.format(hit['peptide'], hit['dom_name'])})

    # add wether it is in Epifactors DB, or not;

    species = species.split('/')[3]

    if matches: # Sometimes it's empty;
        gl = genelist()
        gl.load_list(matches)
        gl = gl.removeDuplicates('unq_key')
        gl = gl.getColumns(['ensp', 'e', 'domain'])
        gl.saveTSV('model_hits/{0}.matches.tsv'.format(species), key_order=['ensp', 'domain', 'e'])
        gl.save('model_hits_glbs/{0}.matches.glb'.format(species))
