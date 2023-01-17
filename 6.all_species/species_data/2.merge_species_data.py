#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *

'''

There are mismatches in the Ensembl annotations and the actual FASTAs avaiable.

Fix that here by making the union of the two and only keeping species found in both
datasets.

'''


all_species = glload('species_annotations/species.glb')

newl = []

for file in glob.glob('pep_counts/*.txt'):
    oh = open(file, 'rt')
    count = int(oh.readline().split()[0])
    oh.close()

    species_name = os.path.split(file)[1].split('.')[0].lower() # seems a simple rule
    assembly_name = os.path.split(file)[1].replace('.txt', '')

    if count < 5000:
        continue

    newl.append({'species': species_name, 'assembly_name': assembly_name, 'num_pep': count})

pep_counts = genelist()
pep_counts.load_list(newl)

all_species = all_species.map(genelist=pep_counts, key='species')

all_species = all_species.removeDuplicates('name')

print(all_species)
all_species = all_species.getColumns(['name', 'species', 'division' ,'num_pep', 'assembly_name'])

all_species.sort('name')

all_species.saveTSV('all_species.tsv')
all_species.save('all_species.glb')

# and add the peptide counts for all species
