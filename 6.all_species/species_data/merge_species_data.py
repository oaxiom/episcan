#!/usr/bin/env python3
import sys, os, glob
from glbase3 import *


species_annotation = glload('species_annotations/species.glb')
common_names = glload('common_names/common_names.glb')

all_species = species_annotation.map(genelist=common_names, key='name')

newl = []

for file in glob.glob('pep_counts/*.txt'):
    oh = open(file, 'rt')
    count = int(oh.readline().split()[0])
    oh.close()

    species_name = os.path.split(file)[1].split('.')[0].lower() # seems a simple rule
    assembly_name = os.path.split(file)[1].replace('.txt', '')

    newl.append({'species': species_name, 'assembly_name': assembly_name, 'num_pep': count})

pep_counts = genelist()
pep_counts.load_list(newl)

all_species = all_species.map(genelist=pep_counts, key='species')

all_species.saveTSV('all_species.tsv')
all_species.save('all_species.glb')

# and add the peptide counts for all species
