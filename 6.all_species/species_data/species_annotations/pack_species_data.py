#!/usr/bin/env python3
import sys, os, glob, re
from glbase3 import *

form = {'force_tsv': True, 'name': 0, 'species': 1}

table = []

for f in glob.glob('*.txt'):
    base = f.replace('.txt', '').replace('species_Ensembl', '')
    species = genelist(f, format=form)

    for line in species:
        # Trim any assembly details;
        print(line['name'])
        t = re.split(' |_', line['name'])[0:2]

        print(t)
        if len(t) == 2:
            name = '{0} {1}'.format(*t)
        elif len(t) == 1:
            name = t[0]

        table.append({'name': name, 'map_name': line['name'], 'division': base, 'species': line['species']})

all_species = genelist()
all_species.load_list(table)
all_species = all_species.removeDuplicates('name')
all_species.saveTSV('species.tsv')
all_species.save('species.glb')
