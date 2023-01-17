#!/usr/bin/env python3
import sys, os, glob, gzip
from glbase3 import *

'''

There are mismatches in the Ensembl annotations and the actual FASTAs avaiable.

Fix that here by making the union of the two and only keeping species found in both
datasets.

'''

all_species = glload('species_annotations/species.glb')

newl = []

for file in glob.glob('species_fastas/fastas/*.fa.gz'):
    #species_name = os.path.split(file)[1].split('.')[0].lower() # seems a simple rule
    assembly_name = os.path.split(file)[1].replace('.fa.gz', '')


    oh = gzip.open(file, 'r')
    count = len(oh.readlines())
    oh.close()

    newl.append({'assembly_name': assembly_name, 'num_pep': count})

    print(assembly_name, count)

pep_counts = genelist()
pep_counts.load_list(newl)

all_species.saveTSV('num_peps.tsv')
all_species.save('num_peps.glb')

# and add the peptide counts for all species
