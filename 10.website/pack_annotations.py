
import sys, os, glob, gzip
from glbase3 import *

[os.remove(f) for f in glob.glob('annotations/*.glb')]
[os.remove(f) for f in glob.glob('annotations_tsv/*.tsv')]

keep_key = set(['gene_id', 'gene_biotype', 'gene_name'])

species_data = glload('../6.all_species/species_data/all_species.glb')
species_data = set(species_data['assembly_name'])
#print(species_data)

species_found = 0
valid_species = 0

for gtf in glob.glob('annotation_data/*/*/*.gtf.gz') + glob.glob('annotation_data/*/*/*/*.gtf.gz'):
    if 'chr.' in gtf:
        continue
    if 'abinitio.' in gtf:
        continue

    species_found += 1

    assembly_name = os.path.split(gtf)[1].replace('.47.gtf.gz', '') # 47 is the release number

    print(assembly_name)

    if assembly_name not in species_data:
        continue

    valid_species += 1

    print('Doing {0}'.format(gtf))

    oh = gzip.open(gtf, 'rt')

    gtf_data = []

    for line in oh:
        if line[0] == '#':
            continue
        t = line.strip().rstrip(';').split('\t')
        if t[2] == 'gene': # Only interested in the annotations
            anns = t[-1].split('; ')
            annotations = {}
            for item in anns:
                k, v = item.split(' "')
                v = v.replace('"', '')
                annotations[k] = v # = {k: v for k, v in zip(k, v)}

        keeps = {}
        for a in annotations:
            if a in keep_key:
                keeps[a] = annotations[a]

        gtf_data.append(keeps)
    oh.close()


    # Save the kept keys:
    gl = genelist()
    gl.load_list(gtf_data)
    gl = gl.removeDuplicates('gene_id')
    gl.save('annotations/{0}.glb'.format(assembly_name))
    gl.saveTSV('annotations_tsv/{0}.tsv'.format(assembly_name))

print('Found {0} species'.format(species_found))
print('Found {0} valid species'.format(valid_species))
