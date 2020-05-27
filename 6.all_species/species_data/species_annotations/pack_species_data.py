#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *

form = {'force_tsv': True, 'name': 0, 'species': 1, 'taxonomy_id': 3}

table = []

for f in glob.glob('*.txt'):
    base = f.replace('.txt', '').replace('species_Ensembl', '')
    species = genelist(f, format=form)

    for line in species:
        table.append({'name': line['name'], 'division': base, 'species': line['species']})

all_species = genelist()
all_species.load_list(table)
all_species = all_species.removeDuplicates('name')
all_species.saveTSV('species.tsv')
all_species.save('species.glb')
