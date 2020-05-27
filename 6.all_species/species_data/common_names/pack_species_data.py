#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *

form = {'name': 1, 'common_name': 0, 'classification': 2, 'taxonomy_id': 3}
fomr_verts = {'name': 0, 'common_name': 0, 'classification': 2, 'taxonomy_id': 3}
fomr_metaz = {'name': 0, 'common_name': 0, 'classification': 2, 'taxonomy_id': 3}

table = []

for f in glob.glob('*.csv'):
    print(f)
    base = f.replace('.csv', '').replace('Species', '')
    if 'Vertebrate' in f: # Vertebrate exceptionalism!!
        species = genelist(f, format=fomr_verts)
    elif 'Metazoa' in f:
        species = genelist(f, format=fomr_metaz)
    else:
        species = genelist(f, format=form)

    for line in species:
        line.update({'division': base})
        table.append(line)

all_species = genelist()
all_species.load_list(table)
all_species = all_species.removeDuplicates('name')
all_species.saveTSV('common_names.tsv')
all_species.save('common_names.glb')
