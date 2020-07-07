#!/usr/bin/env python3
import sys, os, glob, pickle
from glbase3 import *
config.draw_mode = 'pdf'

sys.path.append('../')
import shared

# get all the motif data;

e = glload('all_data.unnormed.glb')
species_data = glload('../6.all_species/species_data/all_species.glb')

e = species_data.map(genelist=e, key='assembly_name')

for species in e:
    species['conditions'] = [(i/species['num_pep'])*100 for i in species['conditions']]
e._optimiseData()

e.column_Z(False)

e.sort('name')

e.save('all_data.normed.glb')
e.saveTSV('all_data.normed.tsv')
