#!/usr/bin/env python3
import sys, os, glob, pickle
from glbase3 import *
config.draw_mode = 'pdf'

sys.path.append('../')
import shared

# get all the motif data;

oh = open('../7.trees/cluster-domains.pickle', "rb")
all_clusters = pickle.load(oh)
oh.close()

species_data = glload('../6.all_species/species_data/all_species.glb')

species_map = {i['assembly_name']: i for i in species_data}

# in form Clus+Id [motifs]
# repack for fast lookup:
for clus in all_clusters:
    all_clusters[clus] = set(all_clusters[clus])

newe = []

for species in list(glob.glob('../6.all_species/model_hits_glbs/*.glb')):
    data = glload(species)
    data = data.removeDuplicates('ensp')

    assembly_name = os.path.split(species)[1].replace('.matches.glb', '')

    if assembly_name[0] == '_':
        continue # skip these ones;

    # for each species, build an expression table;

    conditions = [0] * len(all_clusters)

    for match in data:
        for i, c in enumerate(all_clusters):
            if match['domain'] in all_clusters[c]:
                conditions[i] += 1

    if assembly_name not in species_map:
        print('{0} not found'.format(assembly_name))
        continue

    newe.append({'assembly_name': assembly_name, 'division': species_map[assembly_name]['division'], 'name': species_map[assembly_name]['name'], 'conditions': conditions})

e = expression(loadable_list=newe, cond_names=['Cluster {0}'.format(i) for i in range(len(all_clusters))])
e.save('all_data.unnormed.unfiltered.glb')

print(e)

e = e.removeDuplicates('name')
e.save('all_data.unnormed.glb')
e.saveTSV('all_data.unnormed.tsv')
